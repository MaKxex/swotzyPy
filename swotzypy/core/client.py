from typing import Optional
from .http import HTTPClient
from .config import ClientConfig
from ..auth.auth import BasicAuth
from ..api.endpoints import OrdersAPI, ParcelshopsAPI, RatesAPI, TrackingAPI

class Client:
    """Main client class implementing Facade pattern for Swotzy API"""
    
    def __init__(
        self,
        public_key: str,
        private_key: str,
        base_url: str = "https://api.swotzy.com",
        timeout: float = 30.0,
        retries: int = 3,
        proxies: Optional[dict] = None
    ):
        self.config = (ClientConfig.builder()
                      .base_url(base_url)
                      .timeout(timeout)
                      .retries(retries)
                      .proxies(proxies)
                      .build())
    
        self.auth = BasicAuth(public_key, private_key)
        
        self._http = HTTPClient(self.config, self.auth)
        
        self.orders = OrdersAPI(self._http)
        self.parcelshops = ParcelshopsAPI(self._http)
        self.rates = RatesAPI(self._http)
        self.tracking = TrackingAPI(self._http)
    
    @classmethod
    def from_config(cls, config: ClientConfig, public_key: str, private_key: str) -> "Client":
        """Create client from existing config"""
        client = cls.__new__(cls)
        client.config = config
        client.auth = BasicAuth(public_key, private_key)
        client._http = HTTPClient(config, client.auth)
        client.orders = OrdersAPI(client._http)
        client.parcelshops = ParcelshopsAPI(client._http)
        client.rates = RatesAPI(client._http)
        client.tracking = TrackingAPI(client._http)
        return client