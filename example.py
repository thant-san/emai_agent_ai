#!/usr/bin/env python3
"""
Example usage of the Email Agent
"""

from agent.email_agent import EmailAgent
from config import setup_environment, get_google_credentials_path, get_token_path, validate_config


def setup_environment_and_validate():
    """Set up environment variables and validate configuration"""
    setup_environment()
    validate_config()


def create_agent():
    """Create and return an EmailAgent instance"""
    return EmailAgent(
        client_secret_path=get_google_credentials_path(),
        token_path=get_token_path()
    )


def example_basic_email():
    """Example: Send a basic email"""
    print("\n=== Example 1: Basic Email ===")
    
    agent = create_agent()
    
    prompt = "Send a professional email to nyansintzaw@gmail.com about testing the email agent"
    result = agent.run(prompt)
    
    print_result(result)


def example_draft_email():
    """Example: Create a draft email"""
    print("\n=== Example 2: Draft Email ===")
    
    agent = create_agent()
    
    prompt = "Draft a friendly email to friend@gmail.com inviting them to dinner this weekend"
    result = agent.run(prompt)
    
    print_result(result)


def example_formal_email():
    """Example: Send a formal email"""
    print("\n=== Example 3: Formal Email ===")
    
    agent = create_agent()
    
    prompt = "Write a formal email to hr@company.com requesting vacation days for next month"
    result = agent.run(prompt)
    
    print_result(result)


def example_with_cc():
    """Example: Email with CC"""
    print("\n=== Example 4: Email with CC ===")
    
    agent = create_agent()
    
    prompt = "Send an email to client@company.com about project updates, cc manager@company.com"
    result = agent.run(prompt)
    
    print_result(result)


def print_result(result):
    """Print the result in a formatted way"""
    if result["ok"]:
        print(f"✅ Success: Email {result['mode']}")
        print(f"📧 To: {result['to']}")
        print(f"📋 Subject: {result['subject']}")
        print(f"📄 Preview: {result['preview']['plain'][:150]}...")
        if result['mode'] == 'draft':
            print(f"📝 Draft ID: {result['draft_id']}")
        else:
            print(f"📤 Message ID: {result['message_id']}")
    else:
        print(f"❌ Error: {result['error']}")
        if 'parsed' in result:
            print(f"🔍 Parsed data: {result['parsed']}")


def interactive_mode():
    """Interactive mode for testing"""
    print("\n=== Interactive Mode ===")
    print("Enter email prompts (type 'quit' to exit):")
    
    agent = create_agent()
    
    while True:
        try:
            prompt = input("\n📝 Enter your email prompt: ").strip()
            if prompt.lower() in ['quit', 'exit', 'q']:
                break
            if not prompt:
                continue
                
            result = agent.run(prompt)
            print_result(result)
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


def main():
    """Main function"""
    setup_environment_and_validate()
    
    print("🤖 AI Email Agent Examples")
    print("=" * 50)
    
    # Run examples
    example_basic_email()
    example_draft_email()
    example_formal_email()
    example_with_cc()
    
    # Interactive mode
    interactive_mode()


if __name__ == "__main__":
    main()
