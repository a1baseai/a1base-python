# A1Base Python Client

[![PyPI version](https://badge.fury.io/py/a1base.svg)](https://badge.fury.io/py/a1base)
[![Python Support](https://img.shields.io/pypi/pyversions/a1base.svg)](https://pypi.org/project/a1base/)
[![License](https://img.shields.io/github/license/a1base/a1base-python.svg)](https://github.com/a1base/a1base-python/blob/main/LICENSE)

A powerful and easy-to-use Python client for interacting with the A1Base API. Give your AI agents a phone number, an email, and real autonomy on the internet.

## Features

- Send individual messages via WhatsApp
- Send group messages with attachments
- Retrieve message and thread details
- Get recent messages from threads
- Handle incoming WhatsApp messages
- Email integration
- Built-in security features:
  - HTTPS-only communication
  - Rate limiting
  - Input sanitization
  - Webhook security
  - Safe error handling

## Installation 
bash
pip install a1base
## Quick Start

```python
from a1base import A1BaseClient
from a1base.models import MessageRequest, EmailRequest
from a1base.exceptions import AuthenticationError, ValidationError

# Initialize client
client = A1BaseClient(
    api_key="your_api_key",
    api_secret="your_api_secret"
)

# Send a WhatsApp message
try:
    message = MessageRequest(
        content="Hello, World!",
        from_="+1234567890",
        to="+0987654321",
        service="whatsapp"
    )
    response = client.send_individual_message("your_account_id", message)
    print(f"Message status: {response['status']}")
except AuthenticationError:
    print("Invalid API credentials")
except ValidationError as e:
    print(f"Invalid request: {str(e)}")

# Send an email
try:
    email = EmailRequest(
        sender_address="jane@a101.bot",
        recipient_address="john@a101.bot",
        subject="Hello from Jane",
        body="Have a nice day!",
        headers={
            "cc": ["sarah@a101.bot"],
            "bcc": ["jim@a101.bot"],
            "reply-to": "jane@a101.bot"
        }
    )
    result = client.send_email("your_account_id", email)
    print(f"Email status: {result['status']}")
except ValidationError as e:
    print(f"Invalid email request: {str(e)}")

# Get thread details and recent messages
try:
    # Get thread details
    thread_details = client.get_thread_details("your_account_id", "thread_123")
    print(f"Thread type: {thread_details['chat_type']}")
    print(f"Participants: {thread_details['participants']}")
    
    # Get recent messages
    messages = client.get_recent_messages("your_account_id", "thread_123")
    for msg in messages['messages']:
        print(f"From: {msg['sender_number']}, Content: {msg['content']}")
except Exception as e:
    print(f"Error: {str(e)}")
```

## Advanced Usage

### Group Messaging

```python
from a1base.models import GroupMessageRequest

group_message = GroupMessageRequest(
    content="Hello team!",
    from_="+1234567890",
    service="whatsapp",
    attachment_uri="https://example.com/file.pdf"  # Optional attachment
)
response = client.send_group_message("your_account_id", group_message)
print(f"Group message status: {response['status']}")
```

### Managing Threads

```python
# Get all threads
threads = client.get_all_threads("your_account_id")
print(f"Total threads: {threads['total_count']}")

# Get threads for specific number
number_threads = client.get_threads_by_phone("your_account_id", "+1234567890")
for thread in number_threads['threads']:
    print(f"Thread ID: {thread['thread_id']}")
    print(f"Last message: {thread['last_message']['content']}")
```

### Webhook Handling

```python
# Handle incoming WhatsApp webhook
webhook_data = {
    "external_thread_id": "3456098@s.whatsapp",
    "external_message_id": "2asd5678cfvgh123",
    "chat_type": "individual",
    "content": "Hello!",
    "sender_name": "John",
    "sender_number": "+1234567890",
    "participants": ["+1234567890", "+0987654321"],
    "timestamp": 1734486451000
}

try:
    result = client.handle_whatsapp_incoming(webhook_data)
    print(f"Webhook processed: {result['status']}")
except ValidationError as e:
    print(f"Invalid webhook data: {str(e)}")
```


## Documentation

### Available Methods

- `send_individual_message(account_id, message)`: Send a message to an individual
- `send_group_message(account_id, message)`: Send a message to a group
- `get_individual_message_details(account_id, message_id)`: Get details of a specific message
- `get_recent_messages(account_id, thread_id)`: Get recent messages from a thread
- `get_thread_details(account_id, thread_id)`: Get details about a specific thread
- `get_all_threads(account_id)`: Get all threads for an account
- `get_threads_by_phone(account_id, phone_number)`: Get threads filtered by phone number
- `send_email(account_id, email)`: Send an email
- `create_email(account_id, email)`: Create an email draft
- `handle_whatsapp_incoming(data)`: Process incoming WhatsApp webhook

For detailed API documentation, visit [docs.a1base.com](https://docs.a1base.com)

### Error Handling

The client provides several custom exceptions for proper error handling:

- `AuthenticationError`: Raised when API credentials are invalid
- `ValidationError`: Raised when request data is invalid
- `RateLimitError`: Raised when API rate limits are exceeded
- `A1BaseError`: Base exception for general API errors

Example error handling:

```python
from a1base.exceptions import AuthenticationError, ValidationError, RateLimitError

try:
    response = client.send_individual_message(account_id, message)
except AuthenticationError:
    print("Please check your API credentials")
except ValidationError as e:
    print(f"Invalid request data: {str(e)}")
except RateLimitError:
    print("Rate limit exceeded. Please try again later")
except A1BaseError as e:
    print(f"An error occurred: {str(e)}")
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
