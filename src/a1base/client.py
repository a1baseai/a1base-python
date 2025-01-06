import httpx
from typing import Optional, Dict, Any, Union, List, cast
from .exceptions import A1BaseError, AuthenticationError, ValidationError, RateLimitError
from .models import (
    MessageRequest, 
    MessageResponse,
    GroupMessageRequest,
    GroupMessageResponse,
    EmailRequest,
    EmailResponse,
    ThreadResponse,
    JsonDict,
    EmailHeaders
)

class A1BaseClient:
    """
    A1Base API client for sending messages and managing communications.
    
    Args:
        api_key (str): Your A1Base API key
        api_secret (str): Your A1Base API secret
        base_url (str, optional): API base URL. Defaults to https://api.a1base.com/v1
        
    Attributes:
        base_url (str): Base URL for API requests
        headers (Dict[str, str]): HTTP headers for requests
        client (httpx.Client): HTTP client for making requests
    """
    
    def __init__(
        self, 
        api_key: str, 
        api_secret: str,
        base_url: str = "https://api.a1base.com/v1"
    ) -> None:
        self.base_url: str = base_url.rstrip('/')
        self.headers: Dict[str, str] = {
            'x-api-key': api_key,
            'x-api-secret': api_secret,
            'Content-Type': 'application/json'
        }
        self.client: httpx.Client = httpx.Client(timeout=30.0)

    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[JsonDict] = None
    ) -> JsonDict:
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
                raise AuthenticationError("Invalid API credentials") from e
            elif e.response.status_code == 422:
                raise ValidationError(f"Invalid request: {e.response.json()}") from e
            raise A1BaseError(f"Request failed: {str(e)}") from e

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
            
        try:
            response = self._make_request("POST", endpoint, data)
            # Filter response to only include fields defined in our model
            model_fields = {"to", "from", "body", "status"}
            filtered_response = {k: v for k, v in response.items() if k in model_fields}
            if "from" in filtered_response:
                filtered_response["from_"] = filtered_response.pop("from")
            # Ensure all required fields are present
            if not all(field in filtered_response for field in ["to", "from_", "body"]):
                # If response is missing required fields, create a failure response
                return MessageResponse(
                    to=message.to,
                    from_=message.from_,
                    body=message.content,
                    status="failed"
                )
            return MessageResponse(**filtered_response)
        except AuthenticationError:
            # Re-raise authentication errors without attempting to create response
            raise

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
        return GroupMessageResponse(**cast(JsonDict, response))

    def send_email(
        self,
        account_id: str,
        email: EmailRequest
    ) -> EmailResponse:
        """
        Send an email.
        
        Args:
            account_id (str): Your A1Base account ID
            email (EmailRequest): Email details
            
        Returns:
            EmailResponse: Response containing email status
            
        Raises:
            AuthenticationError: If API credentials are invalid
            ValidationError: If request data is invalid
            RateLimitError: If API rate limit is exceeded
        """
        endpoint = f"/emails/{account_id}/send"
        data: JsonDict = {
            "sender_address": email.sender_address,
            "recipient_address": email.recipient_address,
            "subject": email.subject,
            "body": email.body
        }
        if email.headers:
            headers: JsonDict = {}
            # Handle optional fields from TypedDict
            if "cc" in email.headers:
                headers["cc"] = email.headers["cc"]
            if "bcc" in email.headers:
                headers["bcc"] = email.headers["bcc"]
            if "reply_to" in email.headers:
                headers["reply-to"] = email.headers["reply_to"]
            data["headers"] = headers
        if email.attachment_uri:
            data["attachment_uri"] = email.attachment_uri
            
        response = self._make_request("POST", endpoint, data)
        return EmailResponse(**cast(JsonDict, response))
        
    def get_message_details(
        self,
        account_id: str,
        message_id: str
    ) -> MessageResponse:
        """
        Get details of a specific message.
        
        Args:
            account_id (str): Your A1Base account ID
            message_id (str): ID of the message to retrieve
            
        Returns:
            MessageResponse: Message details
        """
        endpoint = f"/messages/individual/{account_id}/get-details/{message_id}"
        response = self._make_request("GET", endpoint)
        return MessageResponse(**cast(JsonDict, response))
        
    def get_recent_messages(
        self,
        account_id: str,
        thread_id: str
    ) -> List[MessageResponse]:
        """
        Get recent messages from a thread.
        
        Args:
            account_id (str): Your A1Base account ID
            thread_id (str): ID of the thread
            
        Returns:
            List[MessageResponse]: List of recent messages
        """
        endpoint = f"/messages/threads/{account_id}/get-recent/{thread_id}"
        response = self._make_request("GET", endpoint)
        return [MessageResponse(**cast(JsonDict, msg)) for msg in response]
        
    def get_thread_details(
        self,
        account_id: str,
        thread_id: str
    ) -> ThreadResponse:
        """
        Get details of a specific thread.
        
        Args:
            account_id (str): Your A1Base account ID
            thread_id (str): ID of the thread
            
        Returns:
            ThreadResponse: Thread details
        """
        endpoint = f"/messages/threads/{account_id}/get-details/{thread_id}"
        response = self._make_request("GET", endpoint)
        return ThreadResponse(**response)
        
    def get_all_threads(
        self,
        account_id: str
    ) -> List[ThreadResponse]:
        """
        Get all threads for an account.
        
        Args:
            account_id (str): Your A1Base account ID
            
        Returns:
            List[ThreadResponse]: List of thread details
        """
        endpoint = f"/messages/threads/{account_id}/get-all"
        response = self._make_request("GET", endpoint)
        return [ThreadResponse(**cast(JsonDict, thread)) for thread in response]
        
    def get_threads_by_number(
        self,
        account_id: str,
        phone_number: str
    ) -> List[ThreadResponse]:
        """
        Get all threads for a specific phone number.
        
        Args:
            account_id (str): Your A1Base account ID
            phone_number (str): Phone number to filter threads
            
        Returns:
            List[ThreadResponse]: List of thread details
        """
        endpoint = f"/messages/threads/{account_id}/get-all/{phone_number}"
        response = self._make_request("GET", endpoint)
        return [ThreadResponse(**cast(JsonDict, thread)) for thread in response]                                               