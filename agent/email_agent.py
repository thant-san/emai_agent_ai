# agent/email_agent.py
from __future__ import annotations
from typing import Dict, Any, Optional

from tools.gmail_tool import (
    get_gmail_service,
    get_sender_address,
    create_message,
    send_message,
    create_draft,
)
from tools.email_writer import parse_prompt_to_fields, draft_email


class EmailAgent:
    """
    One-shot agent:
      prompt -> parse -> draft -> send OR draft.
    """

    def __init__(
        self,
        client_secret_path: str = "C:\\Users\\HP\\ai_teacher_assistant\\email_agent_test\\google_crediential.json",
        token_path: str = "token.json",
    ):
        self.service = get_gmail_service(
            client_secret_path=client_secret_path, token_path=token_path
        )
        self.sender = get_sender_address(self.service)

    def run(self, prompt: str, *, default_use_html: bool = True) -> Dict[str, Any]:
        parsed = parse_prompt_to_fields(prompt)

        to_email = (parsed.get("to_email") or "").strip()
        if not to_email:
            return {"ok": False, "error": "No recipient email found in the prompt.", "parsed": parsed}

        instruction = parsed.get("notes") or prompt
        drafted = draft_email(parsed.get("to_name", ""), instruction, parsed.get("tone", "professional, friendly"))

        subject = parsed.get("subject_override") or drafted["subject"]
        body_html = drafted["html"] if (default_use_html and drafted["html"]) else None
        body_text = drafted["plain"]
        cc = parsed.get("cc") or None
        bcc = parsed.get("bcc") or None
        action = parsed.get("action")
        action = action if action in ("send", "draft") else "send"

        msg = create_message(
            to=to_email,
            subject=subject,
            body_html=body_html,
            body_text=body_text,
            cc=cc,
            bcc=bcc,
            attachments=None,
            sender=self.sender,
        )

        if action == "draft":
            res = create_draft(self.service, message=msg)
            return {
                "ok": True,
                "mode": "draft",
                "draft_id": res.get("id"),
                "to": to_email,
                "subject": subject,
                "preview": {"plain": body_text},
            }
        else:
            res = send_message(self.service, message=msg)
            return {
                "ok": True,
                "mode": "send",
                "message_id": res.get("id"),
                "to": to_email,
                "subject": subject,
                "preview": {"plain": body_text},
            }
