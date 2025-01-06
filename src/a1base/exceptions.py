class A1BaseError(Exception):
    """Base exception for A1Base errors"""
    pass

class AuthenticationError(A1BaseError):
    """Raised when authentication fails"""
    pass

class ValidationError(A1BaseError):
    """Raised when request validation fails"""
    pass

class RateLimitError(A1BaseError):
    """Raised when rate limit is exceeded"""
    pass 