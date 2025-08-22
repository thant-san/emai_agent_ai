# auth_google.py
import base64
import os
import time
import mimetypes
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


# %%
# @title Upload your OAuth client JSON (named client_secret.json)

SCOPES = ["https://www.googleapis.com/auth/gmail.send",  # send emails
          "https://www.googleapis.com/auth/gmail.modify"]  # drafts (optional)

def get_gmail_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())  # type: ignore
        else:
            # Desktop OAuth flow uses a loopback redirect and avoids redirect_uri_mismatch
            flow = InstalledAppFlow.from_client_secrets_file(os.getenv('C:\Users\HP\ai_teacher_assistant\email_agent_test\emai_agent_ai\goolge_crediential.json'), SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    
    return build("gmail", "v1", credentials=creds)


# %%
service = get_gmail_service()
print("✅ Gmail service is ready.")


# %%
