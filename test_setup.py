#!/usr/bin/env python3
"""
Test script to identify setup issues
"""

import os
import sys
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        from agent.email_agent import EmailAgent
        print("✅ EmailAgent imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import EmailAgent: {e}")
        return False
    
    try:
        from config import setup_environment, get_google_credentials_path, get_token_path, validate_config
        print("✅ Config functions imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import config functions: {e}")
        return False
    
    return True

def test_config():
    """Test configuration setup"""
    print("\n🔍 Testing configuration...")
    
    try:
        from config import setup_environment, validate_config, GOOGLE_CREDENTIALS_PATH
        
        # Test environment setup
        setup_environment()
        print("✅ Environment variables set successfully")
        
        # Check if environment variables are set
        required_vars = ["OPENAI_API_KEY", "OPENAI_API_BASE", "PARSER_MODEL", "WRITER_MODEL"]
        for var in required_vars:
            if os.getenv(var):
                print(f"✅ {var} is set")
            else:
                print(f"❌ {var} is not set")
        
        # Check Google credentials file
        if os.path.exists(GOOGLE_CREDENTIALS_PATH):
            print(f"✅ Google credentials file found: {GOOGLE_CREDENTIALS_PATH}")
        else:
            print(f"❌ Google credentials file not found: {GOOGLE_CREDENTIALS_PATH}")
            print("   Please check the path in config.py")
        
        # Test validation
        try:
            validate_config()
            print("✅ Configuration validation passed")
        except ValueError as e:
            print(f"❌ Configuration validation failed: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False
    
    return True

def test_gmail_service():
    """Test Gmail service initialization"""
    print("\n🔍 Testing Gmail service...")
    
    try:
        from tools.gmail_tool import get_gmail_service
        from config import get_google_credentials_path, get_token_path
        
        service = get_gmail_service(
            client_secret_path=get_google_credentials_path(),
            token_path=get_token_path()
        )
        print("✅ Gmail service created successfully")
        
        # Test getting sender address
        from tools.gmail_tool import get_sender_address
        sender = get_sender_address(service)
        print(f"✅ Sender address: {sender}")
        
    except Exception as e:
        print(f"❌ Gmail service test failed: {e}")
        return False
    
    return True

def test_openai_client():
    """Test OpenAI client"""
    print("\n🔍 Testing OpenAI client...")
    
    try:
        from tools.email_writer import _make_client
        
        client = _make_client()
        print("✅ OpenAI client created successfully")
        
    except Exception as e:
        print(f"❌ OpenAI client test failed: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🧪 Email Agent Setup Test")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Configuration", test_config),
        ("Gmail Service", test_gmail_service),
        ("OpenAI Client", test_openai_client),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n🎉 All tests passed! Your setup is ready.")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
