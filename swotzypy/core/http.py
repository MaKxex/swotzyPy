from typing import Optional, Dict, Any
import httpx
import asyncio
from .config import ClientConfig
from ..auth.auth import AuthStrategy

from ..exceptions import (
    SwotzyError,
    ValidationError,
    AddressValidationError,
    RateLimitError,
    AuthenticationError,
    ResourceNotFoundError,
    ServiceUnavailableError
)

class HTTPClient:
    """Low-level HTTP client for handling requests"""
    
    def __init__(self, config: ClientConfig, auth: Optional[AuthStrategy] = None):
        self.config = config
        self.auth = auth
        self._sync_client = self._create_sync_client()
        self._async_client = None  # Lazy initialization for async client
    
    def _create_sync_client(self) -> httpx.Client:
        return httpx.Client(
            timeout=self.config.timeout,
            proxies=self.config.proxies
        )
    
    async def _get_async_client(self) -> httpx.AsyncClient:
        if self._async_client is None:
            self._async_client = httpx.AsyncClient(
                timeout=self.config.timeout,
                proxies=self.config.proxies
            )
        return self._async_client
    
    def _prepare_request(self, endpoint: str, headers: Optional[Dict[str, str]] = None) -> tuple[str, Dict[str, str]]:
        url = self.config.base_url.rstrip('/') + '/' + endpoint.lstrip('/')
        request_headers = {"Accept": "application/json"}
        
        if headers:
            request_headers.update(headers)
        if self.auth:
            request_headers.update(self.auth.get_auth_headers())
            
        return url, request_headers
    
    def _handle_response(self, response: httpx.Response) -> Any:
        """Handle API response and raise appropriate exceptions"""
        if response.is_success:
            return response.json()

        try:
            error_data = response.json()
        except ValueError:
            error_data = {"detail": response.text}

        if response.status_code == 400:
            if "errors" in error_data:
                if "address" in str(error_data.get("type", "")):
                    raise AddressValidationError(error_data["errors"])
                raise ValidationError(error_data["errors"])
            raise SwotzyError(error_data.get("detail", "Bad request"))

        elif response.status_code == 401:
            raise AuthenticationError(error_data.get("detail", "Authentication failed"))

        elif response.status_code == 404:
            resource_type = error_data.get("type", "Resource")
            resource_id = error_data.get("id", "unknown")
            raise ResourceNotFoundError(resource_type, resource_id)

        elif response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 60))
            raise RateLimitError(retry_after)

        elif response.status_code == 503:
            carrier = error_data.get("carrier", "Unknown")
            message = error_data.get("detail")
            raise ServiceUnavailableError(carrier, message)

        else:
            raise SwotzyError(error_data.get("detail", f"HTTP {response.status_code} error"))
    
    # Synchronous methods
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None) -> Any:
        url, headers = self._prepare_request(endpoint, headers)
        response = self._sync_client.get(url, params=params, headers=headers)
        return self._handle_response(response)
    
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None,
             headers: Optional[Dict[str, str]] = None) -> Any:
        url, headers = self._prepare_request(endpoint, headers)
        response = self._sync_client.post(url, json=data, headers=headers)
        return self._handle_response(response)
    
    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None) -> Any:
        url, headers = self._prepare_request(endpoint, headers)
        response = self._sync_client.put(url, json=data, headers=headers)
        return self._handle_response(response)
    
    def delete(self, endpoint: str, headers: Optional[Dict[str, str]] = None) -> Any:
        url, headers = self._prepare_request(endpoint, headers)
        response = self._sync_client.delete(url, headers=headers)
        return self._handle_response(response)
    
    # Asynchronous methods
    async def aget(self, endpoint: str, params: Optional[Dict[str, Any]] = None,
                  headers: Optional[Dict[str, str]] = None) -> Any:
        url, headers = self._prepare_request(endpoint, headers)
        client = await self._get_async_client()
        response = await client.get(url, params=params, headers=headers)
        return self._handle_response(response)
    
    async def apost(self, endpoint: str, data: Optional[Dict[str, Any]] = None,
                   headers: Optional[Dict[str, str]] = None) -> Any:
        url, headers = self._prepare_request(endpoint, headers)
        client = await self._get_async_client()
        response = await client.post(url, json=data, headers=headers)
        return self._handle_response(response)
    
    async def aput(self, endpoint: str, data: Optional[Dict[str, Any]] = None,
                  headers: Optional[Dict[str, str]] = None) -> Any:
        url, headers = self._prepare_request(endpoint, headers)
        client = await self._get_async_client()
        response = await client.put(url, json=data, headers=headers)
        return self._handle_response(response)
    
    async def adelete(self, endpoint: str, headers: Optional[Dict[str, str]] = None) -> Any:
        url, headers = self._prepare_request(endpoint, headers)
        client = await self._get_async_client()
        response = await client.delete(url, headers=headers)
        return self._handle_response(response)
    
    def __del__(self):
        """Cleanup resources"""
        self._sync_client.close()
        if self._async_client:
            asyncio.create_task(self._async_client.aclose())