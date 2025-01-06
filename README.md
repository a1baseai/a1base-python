# A1Base Python Client

[![PyPI version](https://badge.fury.io/py/a1base.svg)](https://badge.fury.io/py/a1base)
[![Python Support](https://img.shields.io/pypi/pyversions/a1base.svg)](https://pypi.org/project/a1base/)
[![License](https://img.shields.io/github/license/a1base/a1base-python.svg)](https://github.com/a1base/a1base-python/blob/main/LICENSE)

A powerful and easy-to-use Python client for interacting with the A1Base API. Give your AI agents a phone number, an email, and real autonomy on the internet.

## Installation

```bash
pip install a1base
```

## Quick Start

```python
from a1base import A1BaseClient
from a1base.models import MessageRequest, EmailRequest

# Initialize client
client = A1BaseClient(
    api_key="your_api_key",
    api_secret="your_api_secret"
)

# Send a WhatsApp message
message = MessageRequest(
    content="Hello, World!",
    from_="+1234567890",
    to="+0987654321",
    service="whatsapp"
)
response = client.send_individual_message("your_account_id", message)
print(f"Message status: {response.status}")

# Send an email
email = EmailRequest(
    sender_address="jane@a101.bot",
    recipient_address="john@a101.bot",
    subject="Hello from A1Base",
    body="Have a nice day!",
    headers={
        "cc": ["sarah@a101.bot"],
        "reply-to": "jane@a101.bot"
    }
)
response = client.send_email("your_account_id", email)
print(f"Email status: {response.status}")
```

## Authentication

The A1Base client uses API key authentication. You'll need both an API key and an API secret:

```python
client = A1BaseClient(
    api_key="your_api_key",
    api_secret="your_api_secret"
)
```

These credentials are automatically included in all API requests as headers.

## Features

### Messaging

#### Send Individual Messages
```python
from a1base.models import MessageRequest

message = MessageRequest(
    content="Your message content",
    from_="+1234567890",  # Sender's phone number
    to="+0987654321",     # Recipient's phone number
    service="whatsapp",   # "whatsapp" or "telegram"
    attachment_uri="https://example.com/file.pdf"  # Optional
)

response = client.send_individual_message("account_id", message)
```

#### Send Group Messages
```python
from a1base.models import GroupMessageRequest

message = GroupMessageRequest(
    content="Group message content",
    from_="+1234567890",
    service="whatsapp",
    attachment_uri="https://example.com/image.jpg"  # Optional
)

response = client.send_group_message("account_id", message)
```

#### Get Message Details
```python
# Get details of a specific message
message_details = client.get_message_details("account_id", "message_id")

# Get recent messages from a thread
recent_messages = client.get_recent_messages("account_id", "thread_id")

# Get thread details
thread_details = client.get_thread_details("account_id", "thread_id")

# Get all threads
all_threads = client.get_all_threads("account_id")

# Get threads for a specific phone number
number_threads = client.get_threads_by_number("account_id", "+1234567890")
```

### Email

#### Send Emails
```python
from a1base.models import EmailRequest

email = EmailRequest(
    sender_address="sender@a101.bot",
    recipient_address="recipient@a101.bot",
    subject="Email Subject",
    body="Email body content",
    headers={
        "bcc": ["bcc@a101.bot"],
        "cc": ["cc@a101.bot"],
        "reply-to": "reply@a101.bot"
    },
    attachment_uri="https://example.com/attachment.pdf"  # Optional
)

response = client.send_email("account_id", email)
```

### Error Handling

The client includes built-in error handling for common scenarios:

```python
from a1base import AuthenticationError, ValidationError, RateLimitError

try:
    response = client.send_individual_message("account_id", message)
except AuthenticationError:
    print("Invalid API credentials")
except ValidationError as e:
    print(f"Invalid request: {e}")
except RateLimitError:
    print("Rate limit exceeded")
```

## Development

To contribute to the project, install development dependencies:

```bash
# Clone the repository
git clone https://github.com/a1baseai/a1base-python.git
cd a1base-python

# Install development dependencies
pip install -r requirements-dev.txt
```

## Security Features

### HTTPS Enforcement
All API communication is enforced over HTTPS to ensure data security in transit.

### Rate Limiting
Built-in rate limiting protects against abuse and ensures fair API usage.

### Input Sanitization
Automatic sanitization of all user inputs:
- Message content validation
- Attachment URI validation
- Phone number format verification
- Service type validation

### Error Handling
Secure error handling implementation:
- Sanitized error messages
- No sensitive data exposure
- Detailed logging
- Custom error types

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
