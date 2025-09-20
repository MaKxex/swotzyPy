from dataclasses import dataclass
from typing import Optional

@dataclass
class ClientConfig:
    """Configuration for the API client using Builder pattern"""
    base_url: str
    timeout: float = 30.0
    retries: int = 3
    proxies: Optional[dict] = None
    
    @classmethod
    def builder(cls) -> "ClientConfigBuilder":
        return ClientConfigBuilder()

class ClientConfigBuilder:
    """Builder for ClientConfig"""
    
    def __init__(self):
        self._base_url = None
        self._timeout = 30.0
        self._retries = 3
        self._proxies = None
    
    def base_url(self, url: str) -> "ClientConfigBuilder":
        self._base_url = url
        return self
    
    def timeout(self, seconds: float) -> "ClientConfigBuilder":
        self._timeout = seconds
        return self
    
    def retries(self, count: int) -> "ClientConfigBuilder":
        self._retries = count
        return self
    
    def proxies(self, proxies: dict) -> "ClientConfigBuilder":
        self._proxies = proxies
        return self
    
    def build(self) -> ClientConfig:
        if not self._base_url:
            raise ValueError("base_url is required")
        return ClientConfig(
            base_url=self._base_url,
            timeout=self._timeout,
            retries=self._retries,
            proxies=self._proxies
        )