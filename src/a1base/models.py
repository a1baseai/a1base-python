from dataclasses import dataclass
from typing import Optional, List, Dict

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
    service: str
    attachment_uri: Optional[str] = None

@dataclass
class EmailRequest:
    sender_address: str
    recipient_address: str
    subject: str
    body: str
    headers: Optional[Dict[str, List[str]]] = None
    attachment_uri: Optional[str] = None 