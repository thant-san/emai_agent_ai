#!/usr/bin/env python3
"""
Email Agent - AI-powered email composition and sending tool
"""

from agent.email_agent import EmailAgent
from config import setup_environment, get_google_credentials_path, get_token_path, validate_config


def main():
    """Main function to demonstrate the email agent"""
    
    # Set up environment and validate configuration
    setup_environment()
    validate_config()
    
    # Initialize the email agent
    agent = EmailAgent(
        client_secret_path=get_google_credentials_path(),
        token_path=get_token_path()
    )
    
    print("✅ Email Agent initialized successfully!")
    print(f"📧 Sender: {agent.sender}")
    
    # Example usage
    prompt = "Write an email about testing for email agent to nyansintzaw@gmail.com"
    
    print(f"\n📝 Processing prompt: {prompt}")
    result = agent.run(prompt)
    
    if result["ok"]:
        print(f"✅ Email {result['mode']} successful!")
        print(f"📧 To: {result['to']}")
        print(f"📋 Subject: {result['subject']}")
        print(f"📄 Preview: {result['preview']['plain'][:100]}...")
    else:
        print(f"❌ Error: {result['error']}")


if __name__ == "__main__":
    main()
