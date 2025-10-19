from datetime import datetime
from typing import Optional, List, Dict, Literal
from pydantic import BaseModel, EmailStr
from .enums import (
    DeliveryType, OrderStatus, CarrierEnum, 
    InvoiceType, ExportReason, ShipmentDeliveryStatus, 
    RecipientEntityType, TrackingEventStatus,
    ShipmentPurpose, TaxIdTypes, TermsOfSale,
    OrderSource, DutiesPayor
)

class Address(BaseModel):
    full_name: str
    company: Optional[str] = None
    contact_name: Optional[str] = None
    phone: str
    email: Optional[EmailStr] = None
    address1: str
    address2: Optional[str] = None
    zip: str
    city: str
    state: Optional[str] = None
    country: str


class TaxIds(BaseModel):
    type: TaxIdTypes
    value: str
    country: str

class InvoiceSchema(BaseModel):
    item_discount: Optional[float] = None
    freight_costs: Optional[float] = None
    insurance_costs: Optional[float] = None
    other_costs: Optional[float] = None
    packing_costs: Optional[float] = None
    handling_costs: Optional[float] = None
    invoice_number: Optional[str] = None
    invoice_date: Optional[str] = None


class DeliveryConfigClassic(BaseModel):
    type: Literal[DeliveryType.CLASSIC] = DeliveryType.CLASSIC

class DeliveryConfigParcelshop(BaseModel):
    type: Literal[DeliveryType.PARCELSHOP] = DeliveryType.PARCELSHOP
    parcelshop_id: str

class DeliveryConfigPallet(BaseModel):
    type: Literal[DeliveryType.PALLET] = DeliveryType.PALLET
    pallet_type: str

class PackageComplete(BaseModel):
    length: float
    width: float
    height: float
    weight: float

class ShipmentItem(BaseModel):
    title: str
    quantity: int
    value: float
    sku: Optional[str] = None
    country_of_origin: str
    weight: float
    hs_code: str

class Customs(BaseModel):
    declaration_statement: Optional[str] = None
    other_comments: Optional[str] = None
    duties_payor: Optional[DutiesPayor] = DutiesPayor.RECIPIENT
    incoterms: Optional[TermsOfSale] = None
    third_party_fedex_number: Optional[str] = None
    export_reason: Optional[ExportReason] = ExportReason.SALE
    sender_tax_id: Optional[TaxIds] = None
    recipient_tax_id: Optional[TaxIds] = None
    importer_tax_id: Optional[TaxIds] = None
    importer_address: Optional[Address] = None
    invoice: Optional[InvoiceSchema] = None

class ShipmentBase(BaseModel):
    package: PackageComplete
    customs_items: Optional[List[ShipmentItem]] = None

class ShipmentOut(BaseModel):
    id: int
    tracking_number: Optional[str] = None
    tracking_url: Optional[str] = None
    carrier_tracking_url: Optional[str] = None
    delivery_status: Optional[ShipmentDeliveryStatus] = None

class DeliveryEstimate(BaseModel):
    from_date: datetime
    to_date: datetime

class ParcelshopLocation(BaseModel):
    id: str
    display_name: str
    street: str
    city: str
    zip: str
    country: str
    latitude: float
    longitude: float

class OrderBase(BaseModel):
    carrier: Optional[CarrierEnum] = None
    service: Optional[str] = None
    reference_id: Optional[str] = None
    delivery_config: DeliveryConfigClassic | DeliveryConfigParcelshop | DeliveryConfigPallet
    address_sender: Address
    address_recipient: Address
    shipments: List[ShipmentBase]

class Order(OrderBase):
    id: int
    source: OrderSource
    status: OrderStatus
    subtotal: Optional[float] = None
    currency: str
    date_created: datetime
    delivery_estimate: Optional[str] = None
    shipments: List[ShipmentOut]
    is_active: bool

class OrderCreate(OrderBase):
    pass


class TrackingEvent(BaseModel):
    status: TrackingEventStatus
    timestamp: datetime
    description: str
    location: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    zip: Optional[str] = None

class TrackingInfo(BaseModel):
    tracking_number: str
    carrier: Optional[CarrierEnum] = None
    events: List[TrackingEvent]
    delivery_status: Optional[ShipmentDeliveryStatus] = None
    date_delivered: Optional[datetime] = None

class FedexImporterOfRecord(BaseModel):
    tax_id: str
    company: str
    phone: str
    address: str
    city: str
    country: str
    zip: str

class Extras(BaseModel):
    fragile: Optional[bool] = False
    return_of_document: Optional[bool] = False
    id_check: Optional[bool] = False
    duties_payor: Optional[DutiesPayor] = None
    fedex_terms_of_sale: Optional[TermsOfSale] = None
    fedex_shipment_purpose: Optional[ShipmentPurpose] = None
    fedex_invoice_type: Optional[InvoiceType] = None
    fedex_declaration_statement: Optional[str] = None
    fedex_importer_of_record: Optional[FedexImporterOfRecord] = None

class RateRequest(BaseModel):
    sender_address: Address
    currency: Optional[str] = "EUR"
    shipments: List[ShipmentBase]
    delivery_config: Optional[DeliveryConfigClassic | DeliveryConfigParcelshop | DeliveryConfigPallet] = None
    carrier: Optional[CarrierEnum] = None
    recipient_entity_type: Optional[RecipientEntityType] = None
    recipient_address: Optional[Address] = None
    extras: Optional[Extras] = None
    customs: Optional[Customs] = None
