from datetime import datetime
from typing import Optional, List, Dict, Literal
from pydantic import BaseModel, EmailStr
from .enums import (
    DeliveryType, OrderStatus, CarrierEnum, 
    InvoiceType, ExportReason, ShipmentDeliveryStatus,
    DocumentType, RecipientEntityType, TrackingEventStatus,
    ShipmentPurpose, TaxIdTypes, TermsOfSale
)

class Address(BaseModel):
    full_name: str
    phone: str
    email: EmailStr
    address1: str
    address2: Optional[str] = None
    zip: str
    city: str
    country: str
    company: Optional[str] = None
    entity_type: Optional[RecipientEntityType] = None
    tax_number: Optional[str] = None

class DeliveryConfigClassic(BaseModel):
    type: Literal[DeliveryType.CLASSIC] = DeliveryType.CLASSIC

class DeliveryConfigParcelshop(BaseModel):
    type: Literal[DeliveryType.PARCELSHOP] = DeliveryType.PARCELSHOP
    parcelshop_id: str

class DeliveryConfigPallet(BaseModel):
    type: Literal[DeliveryType.PALLET] = DeliveryType.PALLET
    pallet_type: str

class PackageBase(BaseModel):
    length: float
    width: float
    height: float
    weight: float

class ShipmentItem(BaseModel):
    description: str
    quantity: int
    value: float
    weight: float
    hs_code: str
    country_of_origin: str

class Customs(BaseModel):
    invoice_type: InvoiceType
    export_reason: ExportReason
    shipment_purpose: Optional[ShipmentPurpose] = None
    terms_of_sale: Optional[TermsOfSale] = None
    tax_id_type: Optional[TaxIdTypes] = None
    tax_id: Optional[str] = None

class ShipmentBase(BaseModel):
    package: PackageBase
    items: Optional[List[ShipmentItem]] = None
    customs: Optional[Customs] = None

class ShipmentOut(BaseModel):
    id: int
    tracking_number: str
    tracking_url: str
    carrier_tracking_url: str
    delivery_status: Optional[ShipmentDeliveryStatus] = None

class DeliveryEstimate(BaseModel):
    from_date: datetime
    to_date: datetime

class ParcelshopLocation(BaseModel):
    id: str
    name: str
    address: str
    city: str
    zip: str
    country: str
    latitude: float
    longitude: float
    working_hours: Dict[str, List[str]]

class OrderBase(BaseModel):
    carrier: CarrierEnum
    service: str
    reference_id: Optional[str] = None
    delivery_config: DeliveryConfigClassic | DeliveryConfigParcelshop | DeliveryConfigPallet
    address_sender: Address
    address_recipient: Address
    shipments: List[ShipmentBase]

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    status: OrderStatus
    subtotal: float
    currency: str
    date_created: datetime
    delivery_estimate: Optional[str] = None
    shipments: List[ShipmentOut]
    is_active: bool

class TrackingEvent(BaseModel):
    status: TrackingEventStatus
    timestamp: datetime
    description: str
    location: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    zip: Optional[str] = None

class TrackingInfo(BaseModel):
    events: List[TrackingEvent]
    latest_status: TrackingEventStatus
    latest_timestamp: datetime
    is_delivered: bool