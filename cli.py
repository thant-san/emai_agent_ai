#!/usr/bin/env python3
"""
Command Line Interface for the Email Agent
"""

import argparse
import sys
from agent.email_agent import EmailAgent
from config import setup_environment, get_google_credentials_path, get_token_path, validate_config


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description="AI Email Agent - Send emails using natural language prompts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py "Send a professional email to john@example.com about the meeting"
  python cli.py "Draft a friendly email to friend@gmail.com inviting them to dinner"
  python cli.py --interactive
        """
    )
    
    parser.add_argument(
        "prompt",
        nargs="?",
        help="Email prompt (e.g., 'Send email to john@example.com about meeting')"
    )
    
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Run in interactive mode"
    )
    
    parser.add_argument(
        "--draft", "-d",
        action="store_true",
        help="Create draft instead of sending"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed output"
    )
    
    args = parser.parse_args()
    
    # Set up environment
    try:
        setup_environment()
        validate_config()
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        sys.exit(1)
    
    # Create agent
    try:
        agent = EmailAgent(
            client_secret_path=get_google_credentials_path(),
            token_path=get_token_path()
        )
        print(f"✅ Email Agent initialized (Sender: {agent.sender})")
    except Exception as e:
        print(f"❌ Failed to initialize Email Agent: {e}")
        sys.exit(1)
    
    # Interactive mode
    if args.interactive:
        run_interactive_mode(agent, args.verbose)
        return
    
    # Single prompt mode
    if not args.prompt:
        print("❌ Please provide a prompt or use --interactive mode")
        parser.print_help()
        sys.exit(1)
    
    # Process the prompt
    if args.draft:
        # Modify prompt to create draft
        prompt = f"Draft {args.prompt}"
    else:
        prompt = args.prompt
    
    result = agent.run(prompt)
    print_result(result, args.verbose)


def run_interactive_mode(agent, verbose=False):
    """Run the agent in interactive mode"""
    print("\n🤖 AI Email Agent - Interactive Mode")
    print("=" * 50)
    print("Enter email prompts (type 'quit' to exit)")
    print("Use 'draft:' prefix to create drafts instead of sending")
    print("Example: 'draft: Write email to john@example.com'")
    print("-" * 50)
    
    while True:
        try:
            prompt = input("\n📝 Enter your email prompt: ").strip()
            
            if prompt.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not prompt:
                continue
            
            result = agent.run(prompt)
            print_result(result, verbose)
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


def print_result(result, verbose=False):
    """Print the result in a formatted way"""
    if result["ok"]:
        print(f"\n✅ Success: Email {result['mode']}")
        print(f"📧 To: {result['to']}")
        print(f"📋 Subject: {result['subject']}")
        
        if verbose:
            print(f"📄 Full content:")
            print("-" * 40)
            print(result['preview']['plain'])
            print("-" * 40)
        else:
            print(f"📄 Preview: {result['preview']['plain'][:150]}...")
        
        if result['mode'] == 'draft':
            print(f"📝 Draft ID: {result['draft_id']}")
        else:
            print(f"📤 Message ID: {result['message_id']}")
    else:
        print(f"\n❌ Error: {result['error']}")
        if verbose and 'parsed' in result:
            print(f"🔍 Parsed data: {result['parsed']}")


if __name__ == "__main__":
    main()
