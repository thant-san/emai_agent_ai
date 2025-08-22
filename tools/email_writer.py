# tools/email_writer.py
from __future__ import annotations
import json
import os
import re
from typing import Dict, Any

from openai import OpenAI


def _make_client() -> OpenAI:
    """
    Uses environment variables:
      - OPENAI_API_KEY (required)
      - OPENAI_API_BASE (optional, for compatible gateways)
    """
    api_key = os.getenv("OPENAI_API_KEY")
    assert api_key, "Set OPENAI_API_KEY in your environment."
    base = os.getenv("OPENAI_API_BASE")  # e.g., https://api.aimlapi.com/v1
    if base:
        return OpenAI(api_key=api_key, base_url=base)
    return OpenAI(api_key=api_key)


PARSER_MODEL = os.getenv("PARSER_MODEL", "gpt-4o-mini")
WRITER_MODEL = os.getenv("WRITER_MODEL", "gpt-4o-mini")


def parse_prompt_to_fields(prompt: str) -> Dict[str, str]:
    """
    Return: {to_email, to_name, tone, cc, bcc, action, subject_override, notes}
    action: 'send' | 'draft' (default 'send')
    """
    client = _make_client()

    system_prompt = (
        "Extract email-send intent from a single user instruction. "
        "Return compact JSON with keys: to_email, to_name, tone, cc, bcc, action, subject_override, notes. "
        "cc/bcc must be comma-separated strings or empty. "
        "If an item is missing, set it to an empty string. DO NOT invent emails."
    )

    resp = client.chat.completions.create(
        model=PARSER_MODEL,
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0,
    )
    data = json.loads(resp.choices[0].message.content)

    # Fallback: regex email if model missed it
    if not data.get("to_email"):
        m = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", prompt)
        if m:
            data["to_email"] = m.group(0)

    # Normalize defaults
    data["action"] = (data.get("action") or "send").lower()
    data["tone"] = data.get("tone") or "professional, friendly"
    for k in ("cc", "bcc", "to_name", "subject_override", "notes"):
        data[k] = (data.get(k) or "").strip()
    return data


def draft_email(to_name: str, instruction: str, tone: str = "professional, friendly") -> Dict[str, str]:
    """
    Returns: {subject, plain, html}
    """
    client = _make_client()

    system_prompt = "You write concise, polite emails. Return JSON with keys: subject, plain, html."
    usr = f"""
Recipient name: {to_name or 'there'}
Instruction / purpose: {instruction}
Tone: {tone}
Length: 120-180 words. Avoid flowery language.
"""
    resp = client.chat.completions.create(
        model=WRITER_MODEL,
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": usr}],
        response_format={"type": "json_object"},
        temperature=0.4,
    )
    data = json.loads(resp.choices[0].message.content)
    return {
        "subject": data.get("subject", "Hello"),
        "plain": data.get("plain") or data.get("body", ""),
        "html": data.get("html", ""),
    }
