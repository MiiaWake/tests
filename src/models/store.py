from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from datetime


import datetime, date
from enum import Enum

class OrderStatus(str, Enum):
    PLACED = "placed"
    APPROVED = "approved"
    DELIVERED = "delivered"

class Order(BaseModel):
    id: Optional[int] = None
    petId: int = Field(..., gt=0, description="ID of the pet")
    quantity: int = Field(..., ge=1, le=100, description="Quantity ordered")
    shipDate: Optional[datetime] = None
    status: OrderStatus = Field(..., description="Order status")
    complete: bool = Field(False, description="Is order complete")

    'shipDate', pre=True, always=True
    def set_ship_date(cls, v):
        if v is None:
            return datetime.now()
        return v

    def dict(self, *args, **kwargs) -> Dict[str, Any]:
        kwargs["exclude_none"] = True
        data = super().dict(*args, **kwargs)
        if 'shipDate' in data and isinstance(data['shipDate'], datetime):
            data['shipDate'] = data['shipDate'].isoformat()
        return data

    class Config:
        schema_extra = {
            "example": {
                "id": 12345,
                "petId": 123456789,
                "quantity": 1,
                "shipDate": "2023-12-01T12:00:00.000Z",
                "status": "placed",
                "complete": False
            }
        }

class Inventory(BaseModel):
    available: Optional[int] = 0
    pending: Optional[int] = 0
    sold: Optional[int] = 0

    class Config:
        schema_extra = {
            "example": {
                "available": 5,
                "pending": 2,
                "sold": 10
            }
        }
