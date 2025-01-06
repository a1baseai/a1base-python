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
python
from a1base import A1BaseClient
from a1base.models import MessageRequest
Initialize client
client = A1BaseClient(
api_key="your_api_key",
api_secret="your_api_secret"
)
Send a WhatsApp message
message = MessageRequest(
content="Hello, World!",
from_="+1234567890",
to="+0987654321",
service="whatsapp"
)
response = client.send_individual_message("your_account_id", message)
print(f"Message status: {response.status}")


## Documentation

For detailed documentation, visit [docs.a1base.com](https://docs.a1base.com)

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