import httpx
from typing import Optional, Dict, Any
from .exceptions import A1BaseError, AuthenticationError, ValidationError
from .models import (
    MessageRequest, 
    MessageResponse,
    GroupMessageRequest,
    GroupMessageResponse,
    EmailRequest
)

class A1BaseClient:
    """
    A1Base API client for sending messages and managing communications.
    
    Args:
        api_key (str): Your A1Base API key
        api_secret (str): Your A1Base API secret
        base_url (str, optional): API base URL. Defaults to https://api.a1base.com/v1
    """
    
    def __init__(
        self, 
        api_key: str, 
        api_secret: str,
        base_url: str = "https://api.a1base.com/v1"
    ):
        if not base_url.lower().startswith('https://'):
            raise ValueError('APIService requires HTTPS. Non-HTTPS URLs are not allowed for security reasons.')
            
        self.base_url = base_url.rstrip('/')
        self.headers = {
            'X-API-Key': api_key,
            'X-API-Secret': api_secret,
            'Content-Type': 'application/json'
        }
        self.client = httpx.Client(timeout=30.0)

    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to A1Base API"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.client.request(
                method=method,
                url=url,
                headers=self.headers,
                json=data
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise AuthenticationError("Invalid API credentials")
            elif e.response.status_code == 422:
                raise ValidationError(f"Invalid request: {e.response.json()}")
            raise A1BaseError(f"Request failed: {str(e)}")

    def send_individual_message(
        self, 
        account_id: str, 
        message: MessageRequest
    ) -> MessageResponse:
        """
        Send an individual message via WhatsApp or Telegram.
        
        Args:
            account_id (str): Your A1Base account ID
            message (MessageRequest): Message details
            
        Returns:
            MessageResponse: Response containing message status
        """
        if not message.from_:
            raise ValueError("[A1BaseAPI] Missing 'from' property: a valid 'from' number is required to send an individual message.")

        if not message.content:
            raise ValueError("[A1BaseAPI] Missing 'content' property: 'content' is required to send an individual message.")

        endpoint = f"/messages/individual/{account_id}/send"
        data = {
            "content": message.content,
            "from": message.from_,
            "to": message.to,
            "service": message.service
        }
        if message.attachment_uri:
            data["attachment_uri"] = message.attachment_uri

        response = self._make_request("POST", endpoint, data)
        response_data = response['data']
        # Convert 'from' to 'from_' to match MessageResponse model
        response_data['from_'] = response_data.pop('from')
        return MessageResponse(**response_data)

    def send_group_message(
        self, 
        account_id: str, 
        message: GroupMessageRequest
    ) -> GroupMessageResponse:
        """
        Send a group message.
        
        Args:
            account_id (str): Your A1Base account ID
            message (GroupMessageRequest): Message details
            
        Returns:
            GroupMessageResponse: Response containing message status
        """
        if not message.from_:
            raise ValueError("[A1BaseAPI] Missing 'from' property: a valid 'from' number is required to send a group message.")

        if not message.content:
            raise ValueError("[A1BaseAPI] Missing 'content' property: 'content' is required to send a group message.")

        endpoint = f"/messages/group/{account_id}/send"
        data = {
            "content": message.content,
            "from": message.from_,
            "thread_id": message.thread_id,
            "service": message.service
        }
        if message.attachment_uri:
            data["attachment_uri"] = message.attachment_uri
            
        response = self._make_request("POST", endpoint, data)
        return GroupMessageResponse(**response['data'])

    # Additional methods following similar pattern... 