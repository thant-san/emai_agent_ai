#!/usr/bin/env python3
"""
Configuration settings for the Email Agent
"""

import os
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent

# Google OAuth Configuration
GOOGLE_CREDENTIALS_PATH = str(PROJECT_ROOT / "google_crediential.json")
TOKEN_PATH = PROJECT_ROOT / "token.json"

# Gmail API Scopes
GMAIL_SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify",
]

# OpenAI Configuration
OPENAI_API_KEY = "bb13adc6deb74e9eb2ff033941bd7a34"
OPENAI_API_BASE = "https://api.aimlapi.com/v1"
PARSER_MODEL = "openai/gpt-4o"
WRITER_MODEL = "openai/gpt-4o"

# Email Configuration
DEFAULT_TONE = "professional, friendly"
DEFAULT_USE_HTML = True
MAX_RETRIES = 5
RATE_LIMIT_BACKOFF = 1.5

# File paths
ATTACHMENTS_DIR = PROJECT_ROOT / "attachments"
LOGS_DIR = PROJECT_ROOT / "logs"

# Create directories if they don't exist
ATTACHMENTS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)


def setup_environment():
    """Set up environment variables from config"""
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    os.environ["OPENAI_API_BASE"] = OPENAI_API_BASE
    os.environ["PARSER_MODEL"] = PARSER_MODEL
    os.environ["WRITER_MODEL"] = WRITER_MODEL


def get_google_credentials_path():
    """Get the Google credentials file path"""
    return GOOGLE_CREDENTIALS_PATH


def get_token_path():
    """Get the token file path"""
    return str(TOKEN_PATH)


def validate_config():
    """Validate configuration settings"""
    errors = []
    
    # Check if Google credentials file exists
    if not os.path.exists(GOOGLE_CREDENTIALS_PATH):
        errors.append(f"Google credentials file not found: {GOOGLE_CREDENTIALS_PATH}")
    
    # Check if OpenAI API key is set
    if not OPENAI_API_KEY:
        errors.append("OpenAI API key is not set")
    
    # Check if API base URL is set
    if not OPENAI_API_BASE:
        errors.append("OpenAI API base URL is not set")
    
    if errors:
        raise ValueError("Configuration errors:\n" + "\n".join(f"- {error}" for error in errors))
    
    return True
