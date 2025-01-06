from dataclasses import dataclass
from typing import Optional, List, Dict, Literal, Any, TypedDict, Union

ServiceType = Literal["whatsapp", "telegram"]
MessageStatus = Literal["queued", "sent", "delivered", "failed"]

class EmailHeaders(TypedDict, total=False):
    """Email headers type definition."""
    cc: List[str]
    bcc: List[str]
    reply_to: str  # Maps to "reply-to" in API

JsonDict = Dict[str, Any]

@dataclass
class ThreadResponse:
    """Thread details response model."""
    id: str
    type: str
    participants: List[str]
    created_at: str
    updated_at: str
    messages: List[JsonDict]

@dataclass
class MessageResponse:
    to: str
    from_: str
    body: str
    status: MessageStatus
    message: Optional[str] = None  # Some API responses include a message field

@dataclass
class GroupMessageResponse:
    thread_id: str
    body: str
    status: MessageStatus

@dataclass
class EmailResponse:
    to: str
    from_: str
    subject: str
    body: str
    status: MessageStatus

@dataclass
class MessageRequest:
    content: str
    from_: str
    to: str
    service: ServiceType
    attachment_uri: Optional[str] = None

@dataclass
class GroupMessageRequest:
    content: str
    from_: str
    service: ServiceType
    attachment_uri: Optional[str] = None

@dataclass
class EmailRequest:
    sender_address: str
    recipient_address: str
    subject: str
    body: str
    headers: Optional[EmailHeaders] = None
    attachment_uri: Optional[str] = None              