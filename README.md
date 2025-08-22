# 🤖 AI Email Agent

An intelligent email composition and sending tool that uses AI to draft and send emails based on natural language prompts. Built with Python, Gmail API, and OpenAI GPT models.

## ✨ Features

- 🤖 **AI-powered email composition** using OpenAI GPT models
- 📧 **Gmail integration** for sending emails
- 📝 **Natural language prompt processing** - just describe what you want to send
- 🎯 **Automatic email parsing and drafting**
- 📎 **Support for attachments**
- 📋 **Draft creation option** - create drafts instead of sending
- 🔄 **Rate limiting and retry logic**
- 🖥️ **Multiple interfaces**: CLI, interactive mode, and programmatic API
- 🛡️ **Secure credential management**

## 🏗️ Project Structure

```
emai_agent_ai/
├── agent/
│   └── email_agent.py      # Main EmailAgent class
├── tools/
│   ├── gmail_tool.py       # Gmail API integration
│   └── email_writer.py     # AI email composition
├── config.py               # Centralized configuration
├── main.py                 # Simple entry point
├── example.py              # Usage examples
├── cli.py                  # Command-line interface
├── test_setup.py           # Setup testing
├── find_credentials.py     # Credentials finder
├── debug_error.py          # Error debugging
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── .gitignore             # Git ignore rules
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Google OAuth

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Gmail API
4. Create OAuth 2.0 credentials (Desktop application)
5. Download the credentials JSON file
6. Save it as `google_crediential.json` in your project directory

### 3. Configure OpenAI API

Update `config.py` with your OpenAI API credentials:

```python
OPENAI_API_KEY = "your-openai-api-key"
OPENAI_API_BASE = "https://api.aimlapi.com/v1"  # Optional
```

### 4. Test Setup

```bash
python test_setup.py
```

### 5. Run the Email Agent

```bash
# Simple usage
python main.py

# Interactive CLI
python cli.py --interactive

# Send a specific email
python cli.py "Send a professional email to john@example.com about the meeting tomorrow"
```

## 📖 Usage Examples

### Command Line Interface

```bash
# Send an email
python cli.py "Send a professional email to client@company.com about project updates"

# Create a draft
python cli.py "Draft a friendly email to friend@gmail.com inviting them to dinner"

# Interactive mode
python cli.py --interactive

# Verbose output
python cli.py --verbose "Send email to john@example.com"
```

### Programmatic Usage

```python
from agent.email_agent import EmailAgent
from config import setup_environment, get_google_credentials_path, get_token_path

# Set up environment
setup_environment()

# Initialize the agent
agent = EmailAgent(
    client_secret_path=get_google_credentials_path(),
    token_path=get_token_path()
)

# Send an email
result = agent.run("Write an email to john@example.com about the meeting tomorrow")

if result["ok"]:
    print(f"✅ Email sent to {result['to']}")
    print(f"📋 Subject: {result['subject']}")
else:
    print(f"❌ Error: {result['error']}")
```

### Example Prompts

- `"Send a professional email to client@company.com about project updates"`
- `"Draft a friendly email to friend@gmail.com inviting them to dinner"`
- `"Write a formal email to hr@company.com requesting vacation days"`
- `"Send an email to team@company.com about the new CI/CD pipeline, cc manager@company.com"`

## ⚙️ Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key
- `OPENAI_API_BASE`: Custom API base URL (optional)
- `PARSER_MODEL`: Model for parsing prompts (default: gpt-4o-mini)
- `WRITER_MODEL`: Model for writing emails (default: gpt-4o-mini)

### File Paths

Update these paths in `config.py`:
- `GOOGLE_CREDENTIALS_PATH`: Path to your Google OAuth credentials
- `TOKEN_PATH`: Path to store the OAuth token

## 🔧 Features

### Email Parsing
The agent automatically extracts:
- Recipient email address
- Recipient name
- Email tone
- CC/BCC recipients
- Action (send/draft)
- Subject line
- Additional notes

### Email Composition
- Professional, friendly, or custom tone
- HTML and plain text support
- 120-180 word length
- Context-aware content

### Gmail Integration
- OAuth 2.0 authentication
- Rate limiting protection
- Automatic token refresh
- Draft creation support

## 🛠️ Development

### Testing

```bash
# Run setup tests
python test_setup.py

# Find credentials file
python find_credentials.py

# Debug errors
python debug_error.py
```

### Project Structure

- **`agent/`**: Main agent logic
- **`tools/`**: Utility functions for Gmail and AI
- **`config.py`**: Centralized configuration
- **`cli.py`**: Command-line interface
- **`main.py`**: Simple entry point

## 🔒 Security Notes

- Never commit your API keys or credentials to version control
- Use environment variables for sensitive data
- Keep your OAuth token secure
- Regularly rotate your API keys
- The `.gitignore` file protects sensitive files

## 🐛 Troubleshooting

### Common Issues

1. **Authentication Error**: Check your Google credentials file path
2. **Rate Limit**: The agent automatically retries with exponential backoff
3. **Missing Dependencies**: Run `pip install -r requirements.txt`
4. **API Key Issues**: Verify your OpenAI API key is correct

### Getting Help

If you encounter issues:
1. Run `python test_setup.py` to check your setup
2. Run `python find_credentials.py` to locate credentials
3. Run `python debug_error.py` for detailed error information
4. Check the console output for error messages

## 📝 License

This project is for educational and personal use. Please respect the terms of service for both Google Gmail API and OpenAI API.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

If you need help:
1. Check the troubleshooting section
2. Run the debugging tools
3. Review the configuration
4. Ensure all dependencies are installed

---

**Made with ❤️ using Python, Gmail API, and OpenAI**
