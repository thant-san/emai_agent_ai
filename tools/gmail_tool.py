# tools/gmail_tool.py
from __future__ import annotations
import base64
import mimetypes
import os
import time
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Iterable, Optional, Tuple, Dict, Any

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify",
]


def _guess_mime_type(path: str) -> Tuple[str, str]:
    ctype, encoding = mimetypes.guess_type(path)
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"
    maintype, subtype = ctype.split("/", 1)
    return maintype, subtype


def get_gmail_service(
    client_secret_path: str = None,
    token_path: str = "token.json",
    scopes: Iterable[str] = SCOPES,
):
    """
    Desktop OAuth (loopback) flow; avoids redirect_uri_mismatch.
    Creates/refreshes token.json automatically.
    """
    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, scopes)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            assert os.path.exists(client_secret_path), (
                f"OAuth client file not found: {client_secret_path}"
            )
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secret_path, scopes
            )
            creds = flow.run_local_server(port=0)
        with open(token_path, "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def get_sender_address(service) -> str:
    profile = service.users().getProfile(userId="me").execute()
    return profile.get("emailAddress")


def create_message(
    *,
    to: str,
    subject: str,
    body_html: Optional[str] = None,
    body_text: Optional[str] = None,
    cc: Optional[str] = None,
    bcc: Optional[str] = None,
    attachments: Optional[Iterable[str]] = None,
    sender: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Build a MIME message. Provide body_html OR body_text (or both).
    attachments: iterable of file paths.
    """
    if attachments:
        msg = MIMEMultipart()
        alt = MIMEMultipart("alternative")
        msg.attach(alt)
        if body_text:
            alt.attach(MIMEText(body_text, "plain"))
        if body_html:
            alt.attach(MIMEText(body_html, "html"))
    else:
        if body_html:
            msg = MIMEText(body_html, "html")
        else:
            msg = MIMEText(body_text or "", "plain")

    # Ensure we have a container to set headers cleanly
    if not isinstance(msg, MIMEMultipart):
        container = MIMEMultipart("alternative")
        container.attach(msg)
        msg = container

    msg["To"] = to
    msg["Subject"] = subject
    if sender:
        msg["From"] = sender
    if cc:
        msg["Cc"] = cc
    if bcc:
        msg["Bcc"] = bcc

    # Add attachments
    if attachments:
        for path in attachments:
            path = path.strip()
            if not path:
                continue
            if not os.path.exists(path):
                raise FileNotFoundError(f"Attachment not found: {path}")
            maintype, subtype = _guess_mime_type(path)
            with open(path, "rb") as f:
                part = MIMEBase(maintype, subtype)
                part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition", "attachment", filename=os.path.basename(path)
            )
            msg.attach(part)

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    return {"raw": raw, "bcc": bcc}


def send_message(service, *, user_id: str = "me", message: Dict[str, Any], max_retries: int = 5):
    """
    Sends an email with exponential backoff on rate limits.
    """
    assert message and "raw" in message
    for attempt in range(max_retries):
        try:
            return (
                service.users()
                .messages()
                .send(userId=user_id, body={"raw": message["raw"]})
                .execute()
            )
        except HttpError as e:
            status = getattr(e, "status_code", None) or getattr(getattr(e, "resp", None), "status", None)
            if status in [403, 429]:
                sleep_s = min(30, (1.5 ** attempt))
                print(f"Rate-limited (attempt {attempt+1}/{max_retries}). Sleeping {sleep_s:.1f}s…")
                time.sleep(sleep_s)
                continue
            raise


def create_draft(service, *, user_id: str = "me", message: Dict[str, Any]):
    assert message and "raw" in message
    return (
        service.users()
        .drafts()
        .create(userId=user_id, body={"message": {"raw": message["raw"]}})
        .execute()
    )
