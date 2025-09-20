from abc import ABC, abstractmethod
from typing import Dict
import base64

class AuthStrategy(ABC):
    """Base class for authentication strategies"""
    
    @abstractmethod
    def get_auth_headers(self) -> Dict[str, str]:
        """Returns authentication headers"""
        pass

class BasicAuth(AuthStrategy):
    """Basic authentication strategy for Swotzy API"""
    
    def __init__(self, public_key: str, private_key: str):
        """
        Initialize BasicAuth with API credentials
        
        Args:
            public_key: Swotzy API public key (username)
            private_key: Swotzy API private key (password)
        """
        self.public_key = public_key
        self.private_key = private_key

    def get_auth_headers(self) -> Dict[str, str]:
        """Returns basic auth headers for API requests"""
        credentials = f"{self.public_key}:{self.private_key}"
        encoded = base64.b64encode(credentials.encode()).decode()
        return {
            "Authorization": f"Basic {encoded}",
            "Accept": "application/json"
        }