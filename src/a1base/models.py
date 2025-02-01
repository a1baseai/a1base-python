from dataclasses import dataclass
from typing import Optional, List, Dict, Literal

@dataclass
class MessageResponse:
    to: str
    from_: str
    body: str
    status: str

@dataclass
class GroupMessageResponse:
    thread_id: str
    body: str
    status: str

@dataclass
class MessageRequest:
    content: str
    from_: str
    to: str
    service: str
    attachment_uri: Optional[str] = None

@dataclass
class GroupMessageRequest:
    content: str
    from_: str
    thread_id: str
    service: str
    attachment_uri: Optional[str] = None

@dataclass
class WhatsAppIncomingData:
    thread_id: str
    message_id: str
    thread_type: Literal['individual', 'group', 'broadcast']
    content: str
    sender_number: str
    sender_name: str
    a1_account_id: str
    timestamp: str
    service: Literal['email', 'sms', 'whatsapp']
    a1_account_number: Optional[str] = None
    """ Deprecated: Use a1_account_id instead """
