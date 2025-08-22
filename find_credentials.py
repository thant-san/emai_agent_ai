#!/usr/bin/env python3
"""
Script to help find Google credentials file
"""

import os
from pathlib import Path

def find_google_credentials():
    """Find Google credentials file in common locations"""
    print("🔍 Searching for Google credentials file...")
    
    # Common locations to search
    search_paths = [
        # Current directory
        Path.cwd(),
        # Parent directories
        Path.cwd().parent,
        Path.cwd().parent.parent,
        # User home directory
        Path.home(),
        # Specific paths mentioned in config
        Path("C:\\Users\\HP\\ai_teacher_assistant"),
        Path("C:\\Users\\HP\\ai_teacher_assistant\\email_agent_test"),
        Path("C:\\Users\\HP\\ai_teacher_assistant\\email_agent_test\\emai_agent_ai"),
    ]
    
    # File names to look for
    file_names = [
        "google_crediential.json",
        "client_secret.json", 
        "credentials.json",
        "google_credentials.json",
        "oauth_credentials.json"
    ]
    
    found_files = []
    
    for search_path in search_paths:
        if not search_path.exists():
            continue
            
        print(f"📁 Searching in: {search_path}")
        
        for file_name in file_names:
            file_path = search_path / file_name
            if file_path.exists():
                print(f"✅ Found: {file_path}")
                found_files.append(file_path)
    
    if not found_files:
        print("❌ No Google credentials files found!")
        print("\n💡 Please:")
        print("1. Download your OAuth 2.0 credentials from Google Cloud Console")
        print("2. Save it as 'google_crediential.json' in your project directory")
        print("3. Update the path in config.py")
    else:
        print(f"\n🎉 Found {len(found_files)} credential file(s):")
        for i, file_path in enumerate(found_files, 1):
            print(f"  {i}. {file_path}")
        
        if len(found_files) == 1:
            print(f"\n💡 Update config.py with this path:")
            print(f"   GOOGLE_CREDENTIALS_PATH = r\"{found_files[0]}\"")
    
    return found_files

def check_current_config():
    """Check the current configuration"""
    print("\n🔍 Checking current configuration...")
    
    try:
        from config import GOOGLE_CREDENTIALS_PATH
        
        print(f"Current path in config: {GOOGLE_CREDENTIALS_PATH}")
        
        if os.path.exists(GOOGLE_CREDENTIALS_PATH):
            print("✅ File exists!")
        else:
            print("❌ File not found!")
            
    except ImportError:
        print("❌ Could not import config.py")

if __name__ == "__main__":
    print("🔧 Google Credentials Finder")
    print("=" * 50)
    
    check_current_config()
    find_google_credentials()
