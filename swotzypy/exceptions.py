from typing import List, Dict, Any, Optional

class SwotzyError(Exception):
    """Base exception for all Swotzy API errors"""
    pass

class ValidationError(SwotzyError):
    """Raised when request validation fails"""
    def __init__(self, errors: List[Dict[str, Any]]):
        self.errors = errors
        error_messages = [f"{e['loc']}: {e['msg']}" for e in errors]
        super().__init__(f"Validation error: {'; '.join(error_messages)}")

class AddressValidationError(SwotzyError):
    """Raised when address validation fails"""
    def __init__(self, errors: List[Dict[str, str]]):
        self.errors = errors
        error_messages = [e["message"] for e in errors]
        super().__init__(f"Address validation error: {'; '.join(error_messages)}")

class RateLimitError(SwotzyError):
    """Raised when rate limit is exceeded"""
    def __init__(self, retry_after: int):
        self.retry_after = retry_after
        super().__init__(f"Rate limit exceeded. Try again in {retry_after} seconds")

class AuthenticationError(SwotzyError):
    """Raised when authentication fails"""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message)

class ResourceNotFoundError(SwotzyError):
    """Raised when requested resource is not found"""
    def __init__(self, resource_type: str, resource_id: str):
        self.resource_type = resource_type
        self.resource_id = resource_id
        super().__init__(f"{resource_type} with ID {resource_id} not found")

class ServiceUnavailableError(SwotzyError):
    """Raised when carrier service is temporarily unavailable"""
    def __init__(self, carrier: str, message: Optional[str] = None):
        self.carrier = carrier
        super().__init__(
            message or f"Service for carrier {carrier} is temporarily unavailable"
        )

class WebhookValidationError(SwotzyError):
    """Raised when webhook signature validation fails"""
    def __init__(self):
        super().__init__("Invalid webhook signature")