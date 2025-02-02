# A1Base Python Client

[![PyPI version](https://badge.fury.io/py/a1base.svg)](https://badge.fury.io/py/a1base)
[![Python Support](https://img.shields.io/pypi/pyversions/a1base.svg)](https://pypi.org/project/a1base/)
[![License](https://img.shields.io/github/license/a1base/a1base-python.svg)](https://github.com/a1base/a1base-python/blob/main/LICENSE)

A powerful and easy-to-use Python client for interacting with the [A1Base](https://www.a1base.com) API. Give your AI agents a phone number, an email, and real autonomy on the internet.

---

## Features

- Send individual messages via WhatsApp
- Send group messages with attachments
- Retrieve message and thread details
- Get recent messages from threads
- Handle incoming WhatsApp messages
- Built-in security features:
  - HTTPS-only communication
  - Input sanitization
  - Webhook security
  - Safe error handling

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Importing the Library](#importing-the-library)
  - [Initializing the Client](#initializing-the-client)
- [Security Features](#security-features)
- [API Reference](#api-reference)
  - [Individual Messages](#individual-messages)
  - [Group Messages](#group-messages)
  - [Thread Management](#thread-management)
  - [Webhooks](#webhooks)

## Installation

```bash
pip install a1base
```

## Usage

### Importing the Library

```python
from a1base.client import A1BaseClient
from a1base.models import MessageRequest, GroupMessageRequest
```

### Initializing the Client

```python
client = A1BaseClient(
    api_key="YOUR_API_KEY",
    api_secret="YOUR_API_SECRET"
)
```

## Security Features

### HTTPS Enforcement
All API communication is enforced over HTTPS to ensure data security in transit. The client automatically validates HTTPS URLs.

### Input Sanitization
Automatic validation of all user inputs:
- Message content validation
- Phone number format verification
- Service type validation
- Required field validation

### Error Handling
Secure error handling implementation:
- Custom error types (A1BaseError, AuthenticationError, ValidationError)
- Sanitized error messages
- No sensitive data exposure
- Detailed error information

## API Reference

### Individual Messages

Send an individual message:

```python
message = MessageRequest(
    content="Hello, World!",
    from_="+1234567890",
    to="+0987654321",
    service="whatsapp"
)

response = client.send_individual_message("your_account_id", message)
print(f"Message status: {response.status}")
```

### Group Messages

Send a group message:

```python
message = GroupMessageRequest(
    content="Hello, Group!",
    from_="+1234567890",
    thread_id="thread_123",
    service="whatsapp"
)

response = client.send_group_message("your_account_id", message)
print(f"Message status: {response.status}")
```

### Thread Management

Get all threads:

```python
threads = client.get_all_threads("your_account_id")
print(threads)
```

Get thread details:

```python
thread_details = client.get_thread_details(
    account_id="your_account_id",
    thread_id="thread_123"
)
print(thread_details)
```

Get recent messages:

```python
messages = client.get_recent_messages(
    account_id="your_account_id",
    thread_id="thread_123"
)
print(messages)
```

### Webhooks

Handle incoming WhatsApp messages using Flask:

```python
from flask import Flask, request, jsonify
from a1base.models import WhatsAppIncomingData

app = Flask(__name__)

@app.post("/whatsapp/incoming")
def handle_incoming_message():
    data = WhatsAppIncomingData(**request.json)

    # Handle the message
    return jsonify({"success": True})
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.