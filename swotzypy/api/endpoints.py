from typing import List, Optional, Dict
from ..core.http import HTTPClient
from .models import (
    OrderCreate, Order, ParcelshopLocation,
    TrackingInfo, DeliveryEstimate
)

class OrdersAPI:
    """API methods for working with orders"""
    
    def __init__(self, http_client: HTTPClient):
        self._http = http_client
    
    def get(self, order_id: str) -> Order:
        """Get order by ID"""
        data = self._http.get(f"/public/orders/{order_id}")
        return Order(**self._prepare_order_data(data))
    
    async def aget(self, order_id: str) -> Order:
        """Get order by ID (async)"""
        data = await self._http.aget(f"/public/orders/{order_id}")
        return Order(**self._prepare_order_data(data))
    
    def list(self, page: int = 1, size: int = 100) -> List[Order]:
        """Get list of orders"""
        params = {"page": page, "size": size}
        data = self._http.get("/public/orders", params=params)
        items = data.get("items", [])
        return [Order(**self._prepare_order_data(item)) for item in items]
        
    def _prepare_order_data(self, data: Dict) -> Dict:
        """Prepare order data for model instantiation"""
        try:
            if "delivery_estimate" in data:
                if isinstance(data["delivery_estimate"], dict):
                    data["delivery_estimate"] = DeliveryEstimate(**data["delivery_estimate"])
                elif data["delivery_estimate"] is None:
                    data["delivery_estimate"] = None
                else:
                    pass
            return data
        except Exception as e:
            raise ValueError(f"Error preparing order data: {str(e)}") from e
    
    async def alist(self, page: int = 1, size: int = 100) -> List[Order]:
        """Get list of orders (async)"""
        params = {"page": page, "size": size}
        data = await self._http.aget("/public/orders", params=params)
        items = data.get("items", [])
        return [Order(**self._prepare_order_data(item)) for item in items]
    
    def create(self, order: OrderCreate) -> Order:
        """Create new order"""
        data = order.model_dump()
        response = self._http.post("/public/orders", data=data)
        return Order(**response)
    
    async def acreate(self, order: OrderCreate) -> Order:
        """Create new order (async)"""
        data = order.model_dump()
        response = await self._http.apost("/public/orders", data=data)
        return Order(**response)
    
    def update(self, order_id: str, order: OrderCreate) -> Order:
        """Update existing order"""
        data = order.model_dump()
        response = self._http.put(f"/public/orders/{order_id}", data=data)
        return Order(**response)
    
    async def aupdate(self, order_id: str, order: OrderCreate) -> Order:
        """Update existing order (async)"""
        data = order.model_dump()
        response = await self._http.aput(f"/public/orders/{order_id}", data=data)
        return Order(**response)
    
    def delete(self, order_id: str) -> None:
        """Delete order"""
        self._http.delete(f"/public/orders/{order_id}")
    
    async def adelete(self, order_id: str) -> None:
        """Delete order (async)"""
        await self._http.adelete(f"/public/orders/{order_id}")

class ParcelshopsAPI:
    """API methods for working with parcelshops"""
    
    def __init__(self, http_client: HTTPClient):
        self._http = http_client
    
    def list(self, country: Optional[str] = None, carrier: Optional[str] = None) -> List[ParcelshopLocation]:
        """Get list of parcelshops"""
        params = {}
        if country:
            params["country"] = country
        if carrier:
            params["carriers"] = carrier
            
        data = self._http.get("/public/parcelshops/", params=params)
        return [ParcelshopLocation(**item) for item in data]
    
    async def alist(self, country: Optional[str] = None, carrier: Optional[str] = None) -> List[ParcelshopLocation]:
        """Get list of parcelshops (async)"""
        params = {}
        if country:
            params["country"] = country
        if carrier:
            params["carrier"] = carrier
            
        data = await self._http.aget("/public/parcelshops/", params=params)
        return [ParcelshopLocation(**item) for item in data]

class RatesAPI:
    """API methods for working with shipping rates"""
    
    def __init__(self, http_client: HTTPClient):
        self._http = http_client
    
    def calculate(self, shipment_data: Dict) -> List[Dict]:
        """Calculate shipping rates"""
        response = self._http.post("/public/rates", data=shipment_data)
        return response["rates"]
    
    async def acalculate(self, shipment_data: Dict) -> List[Dict]:
        """Calculate shipping rates (async)"""
        response = await self._http.apost("/public/rates", data=shipment_data)
        return response["rates"]

class TrackingAPI:
    """API methods for tracking shipments"""
    
    def __init__(self, http_client: HTTPClient):
        self._http = http_client
    
    def get_events(self, tracking_number: str) -> TrackingInfo:
        """Get tracking events for a shipment"""
        data = self._http.get(f"/public/tracking/{tracking_number}")
        return TrackingInfo(**data)
    
    async def aget_events(self, tracking_number: str) -> TrackingInfo:
        """Get tracking events for a shipment (async)"""
        data = await self._http.aget(f"/public/tracking/{tracking_number}")
        return TrackingInfo(**data)