from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from enum import Enum
class PetStatus(str, Enum):
    AVAILABLE = "available"
    PENDING = "pending"
    SOLD = "sold"

class Category(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Dogs"
            }
        }

class Tag(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "friendly"
            }
        }

class Pet(BaseModel):
    id: Optional[int] = None
    category: Optional[Category] = None
    name: str = Field(..., min_length=1, max_length=100, description="Pet name")
    photoUrls: List[str] = Field(..., description="List of photo URLs")
    tags: Optional[List[Tag]] = None
    status: Optional[PetStatus] = Field(None, description="pet status in the store")

    'photoUrls'
    def validate_photo_urls(cls, v):
        if not v:
            raise ValueError('At least one photo URL is required')
        return v

    'name'
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()

    def dict(self, *args, **kwargs) -> Dict[str, Any]:
        kwargs["exclude_none"] = True
        return super().dict(*args, **kwargs)

    class Config:
        schema_extra = {
            "example": {
                "id": 123456789,
                "category": {"id": 1, "name": "Dogs"},
                "name": "Doggie",
                "photoUrls": ["http://example.com/photo.jpg"],
                "tags": [{"id": 1, "name": "friendly"}],
                "status": "available"
            }
        }
