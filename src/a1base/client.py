import httpx
import json
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
        self.base_url = base_url.rstrip('/')
        self.headers = {
            'x-api-key': api_key,
            'x-api-secret': api_secret,
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
        return MessageResponse(**response)

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
        endpoint = f"/messages/group/{account_id}/send"
        data = {
            "content": message.content,
            "from": message.from_,
            "service": message.service
        }
        if message.attachment_uri:
            data["attachment_uri"] = message.attachment_uri
            
        response = self._make_request("POST", endpoint, data)
        return GroupMessageResponse(**response)

    def get_individual_message_details(
        self,
        account_id: str,
        message_id: str
    ) -> Dict[str, Any]:
        """
        Get details of an individual message.
        
        Args:
            account_id (str): Your A1Base account ID
            message_id (str): ID of the message to retrieve
            
        Returns:
            Dict[str, Any]: Message details response containing:
                - to: Recipient phone number
                - from: Sender phone number
                - body: Message content
                - status: Message status
        """
        endpoint = f"/messages/individual/{account_id}/get-details/{message_id}"
        return self._make_request("GET", endpoint)

    def get_recent_messages(
        self,
        account_id: str,
        thread_id: str
    ) -> Dict[str, Any]:
        """
        Get recent messages from a thread.
        
        Args:
            account_id (str): Your A1Base account ID
            thread_id (str): ID of the thread to retrieve messages from
            
        Returns:
            Dict[str, Any]: Recent messages response containing list of messages
        """
        endpoint = f"/messages/threads/{account_id}/get-recent/{thread_id}"
        return self._make_request("GET", endpoint)

    def get_thread_details(
        self,
        account_id: str,
        thread_id: str
    ) -> Dict[str, Any]:
        """
        Get details of a chat thread/group.
        
        Args:
            account_id (str): Your A1Base account ID
            thread_id (str): ID of the thread to retrieve
            
        Returns:
            Dict[str, Any]: Thread details response
        """
        endpoint = f"/messages/threads/{account_id}/get-details/{thread_id}"
        return self._make_request("GET", endpoint)

    def get_all_threads(
        self,
        account_id: str
    ) -> Dict[str, Any]:
        """
        Get all threads for an account.
        
        Args:
            account_id (str): Your A1Base account ID
            
        Returns:
            Dict[str, Any]: All threads response
        """
        endpoint = f"/messages/threads/{account_id}/get-all"
        return self._make_request("GET", endpoint)

    def get_threads_by_phone(
        self,
        account_id: str,
        phone_number: str
    ) -> Dict[str, Any]:
        """
        Get all threads for a specific phone number.
        
        Args:
            account_id (str): Your A1Base account ID
            phone_number (str): Phone number to filter threads by
            
        Returns:
            Dict[str, Any]: Filtered threads response
        """
        endpoint = f"/messages/threads/{account_id}/get-all/{phone_number}"
        return self._make_request("GET", endpoint)

    def send_email(
        self,
        account_id: str,
        email: EmailRequest
    ) -> Dict[str, Any]:
        """
        Send an email.
        
        Args:
            account_id (str): Your A1Base account ID
            email (EmailRequest): Email details including:
                - sender_address: Sender email address
                - recipient_address: Recipient email address
                - subject: Email subject
                - body: Email body text
                - headers (optional): Dict with cc, bcc, reply-to
                - attachment_uri (optional): URI of attachment
            
        Returns:
            Dict[str, Any]: Email send response containing:
                - to: Recipient email
                - from: Sender email
                - subject: Email subject
                - body: Email content
                - status: Send status
        """
        endpoint = f"/emails/{account_id}/send"
        data = {
            "sender_address": email.sender_address,
            "recipient_address": email.recipient_address,
            "subject": email.subject,
            "body": email.body
        }
        if email.headers:
            # Convert headers dictionary to JSON string
            data["headers"] = json.dumps({
                key: ",".join(values) if isinstance(values, list) else str(values)
                for key, values in email.headers.items()
            })
        if email.attachment_uri:
            data["attachment_uri"] = email.attachment_uri
            
        return self._make_request("POST", endpoint, data)

    def create_email(
        self,
        account_id: str,
        email: EmailRequest
    ) -> Dict[str, Any]:
        """
        Create an email (draft).
        
        Args:
            account_id (str): Your A1Base account ID
            email (EmailRequest): Email details including:
                - sender_address: Sender email address
                - recipient_address: Recipient email address
                - subject: Email subject
                - body: Email body text
                - headers (optional): Dict with cc, bcc, reply-to
                - attachment_uri (optional): URI of attachment
            
        Returns:
            Dict[str, Any]: Email creation response
        """
        endpoint = f"/emails/{account_id}/create-email"
        data = {
            "sender_address": email.sender_address,
            "recipient_address": email.recipient_address,
            "subject": email.subject,
            "body": email.body
        }
        if email.headers:
            # Convert headers dictionary to JSON string
            data["headers"] = json.dumps({
                key: ",".join(values) if isinstance(values, list) else str(values)
                for key, values in email.headers.items()
            })
        if email.attachment_uri:
            data["attachment_uri"] = email.attachment_uri
            
        return self._make_request("POST", endpoint, data)

    def handle_whatsapp_incoming(
        self,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Handle incoming WhatsApp message webhook.
        
        Args:
            data (Dict[str, Any]): Webhook payload containing:
                - external_thread_id: WhatsApp thread ID
                - external_message_id: WhatsApp message ID
                - chat_type: Type of chat (group/individual/broadcast)
                - content: Message content
                - sender_name: Name of sender
                - sender_number: Phone number of sender
                - participants: List of participant phone numbers
                - a1_account_number: A1Base account number
                - timestamp: Message timestamp
                - secret_key: Webhook secret key
            
        Returns:
            Dict[str, Any]: Webhook handling response
        """
        endpoint = "/wa/whatsapp/incoming"
        return self._make_request("POST", endpoint, data)        