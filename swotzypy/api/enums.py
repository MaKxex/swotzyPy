from enum import Enum

class DeliveryType(str, Enum):
    CLASSIC = "classic"
    PARCELSHOP = "parcelshop"
    PALLET = "pallet"

class OrderStatus(str, Enum):
    DRAFT = "draft"
    READY = "ready"
    WAITING_FOR_PICKUP = "waiting_for_pickup"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DONE = "done"
    CANCELLED = "cancelled"
    RETURNED = "returned"
    LOST = "lost"
    EXPIRED = "expired"
    SHIPPED = "shipped"

class CarrierEnum(str, Enum):
    DPD = "DPD"
    EXPRESS_PASTS = "EXPRESS_PASTS"
    LATVIJAS_PASTS = "LATVIJAS_PASTS"
    OMNIVA = "OMNIVA"
    FEDEX = "FEDEX"
    ITELLA = "ITELLA"
    VENIPAK = "VENIPAK"
    LITHUANIAN_POST = "LITHUANIAN_POST"
    LITHUANIAN_POST_EXPRESS = "LITHUANIAN_POST_EXPRESS"
    UNISEND = "UNISEND"
    UPS = "UPS"
    QWQER = "QWQER"
    NOVAPOST = "NOVAPOST"
    DHL = "DHL"
    DHL_EXPRESS = "DHL_EXPRESS"

class InvoiceType(str, Enum):
    COMMERCIAL_INVOICE = "COMMERCIAL_INVOICE"
    PRO_FORMA_INVOICE = "PRO_FORMA_INVOICE"

class ExportReason(str, Enum):
    GIFT = "GIFT"
    SALE = "SALE"
    SAMPLE = "SAMPLE"
    REPAIR = "REPAIR"
    RETURN = "RETURN"

class ShipmentPurpose(str, Enum):
    GIFT = "GIFT"

class TaxIdTypes(str, Enum):
    VOEC = "VOEC"
    EIN = "EIN"
    VAT = "VAT"
    EORI = "EORI"
    IOSS = "IOSS"
    OTHER = "OTHER"

class TermsOfSale(str, Enum):
    DAP = "DAP"
    DDP = "DDP"

class DocumentType(str, Enum):
    COMMERCIAL_INVOICE = "commercial_invoice"
    PROFORMA_INVOICE = "proforma_invoice"
    CARRIER_INVOICE = "carrier_invoice"

class RecipientEntityType(str, Enum):
    INDIVIDUAL = "individual"
    COMPANY = "company"

class ShipmentDeliveryStatus(str, Enum):
    IN_TRANSIT = "in_transit"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    FAILED = "failed"
    CANCELLED = "cancelled"
    RETURNED = "returned"

class OrderSource(str, Enum):
    API = "api"
    DASHBOARD = "dashboard"
    INTEGRATION = "integration"

class TrackingEventStatus(str, Enum):
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    FAILED = "failed"
    CANCELLED = "cancelled"
    RETURNED = "returned"
    REDIRECTED = "redirected"
    NOTIFICATION = "notification"
    UNKNOWN = "unknown"

class DutiesPayor(str, Enum):
    RECIPIENT = "RECIPIENT"
    SENDER = "SENDER"
    THIRD_PARTY = "THIRD_PARTY"