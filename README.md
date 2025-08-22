# AI Email Agent

An intelligent email composition and sending tool that uses AI to draft and send emails based on natural language prompts.

## Features

- 🤖 AI-powered email composition using OpenAI GPT models
- 📧 Gmail integration for sending emails
- 📝 Natural language prompt processing
- 🎯 Automatic email parsing and drafting
- 📎 Support for attachments
- 📋 Draft creation option
- 🔄 Rate limiting and retry logic

## Project Structure

```
emai_agent_ai/
├── agent/
│   └── email_agent.py      # Main EmailAgent class
├── tools/
│   ├── gmail_tool.py       # Gmail API integration
│   └── email_writer.py     # AI email composition
├── auth_google.py          # Google authentication (legacy)
├── main.py                 # Main entry point
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Gmail API
4. Create OAuth 2.0 credentials (Desktop application)
5. Download the credentials JSON file
6. Place it in your project directory (update path in `main.py`)

### 3. OpenAI API Setup

Set your OpenAI API credentials in `main.py` or as environment variables:

```python
os.environ["OPENAI_API_KEY"] = "your-api-key"
os.environ["OPENAI_API_BASE"] = "https://api.aimlapi.com/v1"  # Optional
```

## Usage

### Basic Usage

```python
from agent.email_agent import EmailAgent

# Initialize the agent
agent = EmailAgent(
    client_secret_path="path/to/your/credentials.json",
    token_path="token.json"
)

# Send an email
result = agent.run("Write an email to john@example.com about the meeting tomorrow")
```

### Command Line Usage

```bash
python main.py
```

## Example Prompts

- "Send a professional email to client@company.com about project updates"
- "Draft a friendly email to friend@gmail.com inviting them to dinner"
- "Write a formal email to hr@company.com requesting vacation days"

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key
- `OPENAI_API_BASE`: Custom API base URL (optional)
- `PARSER_MODEL`: Model for parsing prompts (default: gpt-4o-mini)
- `WRITER_MODEL`: Model for writing emails (default: gpt-4o-mini)

### File Paths

Update these paths in `main.py`:
- `client_secret_path`: Path to your Google OAuth credentials
- `token_path`: Path to store the OAuth token

## Features

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

## Error Handling

The agent includes comprehensive error handling for:
- Missing recipient emails
- API rate limits
- Authentication failures
- File attachment issues

## Security Notes

- Never commit your API keys or credentials to version control
- Use environment variables for sensitive data
- Keep your OAuth token secure
- Regularly rotate your API keys

## Troubleshooting

### Common Issues

1. **Authentication Error**: Check your Google credentials file path
2. **Rate Limit**: The agent automatically retries with exponential backoff
3. **Missing Dependencies**: Run `pip install -r requirements.txt`
4. **API Key Issues**: Verify your OpenAI API key is correct

### Getting Help

If you encounter issues:
1. Check the console output for error messages
2. Verify all file paths are correct
3. Ensure all dependencies are installed
4. Check your internet connection

## License

This project is for educational and personal use. Please respect the terms of service for both Google Gmail API and OpenAI API.
