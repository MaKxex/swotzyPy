# Swotzy API Client

Modern Python client for Swotzy API with support for both synchronous and asynchronous operations.

## Features

- Support for synchronous and asynchronous operations
- Strong typing using Pydantic
- Simple and intuitive interface
- Flexible configuration
- Built-in support for main Swotzy API endpoints
- Support for various courier services

## Installation

```bash
pip install swotzypy
```

### Basic Example

```python
from swotzypy import Client, Address, OrderCreate, DeliveryConfigClassic
from swotzypy.api.enums import CarrierEnum

# Create client with Basic Auth
client = Client(
    public_key="your-public-key",
    private_key="your-private-key"
)

# Create order
order = OrderCreate(
    carrier=CarrierEnum.DPD,
    service="CLASSIC",
    delivery_config=DeliveryConfigClassic(),
    address_sender=Address(
        full_name="John Doe",
        phone="+37122345678",
        email="john@example.com",
        address1="Example street 1",
        zip="LV-1001",
        city="Riga",
        country="LV"
    ),
    address_recipient=Address(
        full_name="Jane Smith",
        phone="+37122345679",
        email="jane@example.com",
        address1="Another street 2",
        zip="LV-1002",
        city="Riga",
        country="LV"
    ),
    shipments=[{
        "package": {
            "length": 20,
            "width": 15,
            "height": 10,
            "weight": 1.5
        }
    }]
)

# Synchronous operations
created_order = client.orders.create(order)
order_details = client.orders.get(created_order.id)
tracking_info = client.tracking.get_events(order_details.shipments[0].tracking_number)

# Asynchronous operations
async def main():
    created_order = await client.orders.acreate(order)
    order_details = await client.orders.aget(created_order.id)
    tracking_info = await client.tracking.aget_events(order_details.shipments[0].tracking_number)
```

### Working with Parcel Points

```python
# Get list of parcel points
parcelshops = client.parcelshops.list(country="LV", carrier="DPD")

# Create order with delivery to parcel point
from swotzypy import DeliveryConfigParcelshop

order = OrderCreate(
    carrier=CarrierEnum.DPD,
    service="PARCELSHOP",
    delivery_config=DeliveryConfigParcelshop(
        parcelshop_id=parcelshops[0].id
    ),
    # ... other fields as in the previous example
)
```


### Configuration Using Builder

```python
from swotzypy import Client, ClientConfig

config = (ClientConfig.builder()
          .base_url("https://api.swotzy.com")
          .timeout(30.0)
          .retries(3)
          .proxies({"http": "http://proxy:8080"})
          .build())

client = Client.from_config(config, 
                          public_key="<your-public-key>",
                          private_key="<your-private-key>")
```

## Architecture

The project follows architecture principles and uses the following design patterns:

- **Facade**: The main `Client` class provides a simple interface for all API capabilities
- **Strategy**: The authentication module supports various authentication strategies (Basic Auth)
- **Builder**: Client configuration is implemented through the Builder pattern

## Modules

### Core

- **client.py**: Implements the Facade pattern, combining all API functionalities
- **http.py**: Low-level layer for handling HTTP requests
- **config.py**: Client configuration using the Builder pattern

### Auth

- **auth.py**: Implements Basic Auth for Swotzy API

### API

- **models.py**: Pydantic models for data typing
- **enums.py**: Enumerations for statuses, delivery types, and courier services
- **endpoints.py**: High-level methods for working with API:
  - Orders: creation and management of orders
  - Parcelshops: working with parcel points
  - Rates: delivery cost calculation
  - Tracking: shipment tracking

## License

MIT