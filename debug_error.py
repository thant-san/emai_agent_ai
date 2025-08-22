#!/usr/bin/env python3
"""
Debug script to catch and display specific errors
"""

import traceback
import sys

def debug_main():
    """Debug version of main.py with detailed error reporting"""
    try:
        print("🔍 Starting debug mode...")
        
        # Test imports
        print("1. Testing imports...")
        from agent.email_agent import EmailAgent
        from config import setup_environment, get_google_credentials_path, get_token_path, validate_config
        print("✅ Imports successful")
        
        # Test configuration
        print("2. Testing configuration...")
        setup_environment()
        validate_config()
        print("✅ Configuration successful")
        
        # Test agent creation
        print("3. Testing agent creation...")
        agent = EmailAgent(
            client_secret_path=get_google_credentials_path(),
            token_path=get_token_path()
        )
        print("✅ Agent creation successful")
        print(f"📧 Sender: {agent.sender}")
        
        # Test email sending
        print("4. Testing email sending...")
        prompt = "Write an email about testing for email agent to nyansintzaw@gmail.com"
        print(f"📝 Processing prompt: {prompt}")
        
        result = agent.run(prompt)
        
        if result["ok"]:
            print(f"✅ Email {result['mode']} successful!")
            print(f"📧 To: {result['to']}")
            print(f"📋 Subject: {result['subject']}")
            print(f"📄 Preview: {result['preview']['plain'][:100]}...")
        else:
            print(f"❌ Error: {result['error']}")
            if 'parsed' in result:
                print(f"🔍 Parsed data: {result['parsed']}")
        
        print("🎉 All tests completed successfully!")
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("💡 This usually means a module is missing or there's a path issue")
        traceback.print_exc()
        
    except FileNotFoundError as e:
        print(f"❌ File Not Found Error: {e}")
        print("💡 This usually means the Google credentials file is missing or in the wrong location")
        traceback.print_exc()
        
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("💡 This usually means there's an issue with your configuration")
        traceback.print_exc()
        
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        print("💡 This is an unexpected error. Here's the full traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    debug_main()
