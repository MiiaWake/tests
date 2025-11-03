from pydantic import BaseModel, Field, validator, EmailStr
from typing import Optional, Dict, Any

class User(BaseModel):
    id: Optional[int] = None
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    firstName: Optional[str] = Field(None, min_length=1, max_length=50, description="First name")
    lastName: Optional[str] = Field(None, min_length=1, max_length=50, description="Last name")
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6, description="Password")
    phone: Optional[str] = Field(None, description="Phone number")
    userStatus: Optional[int] = Field(0, ge=0, description="User status")

    'username'
    def validate_username(cls, v):
        if not v.strip():
            raise ValueError('Username cannot be empty')
        if ' ' in v:
            raise ValueError('Username cannot contain spaces')
        return v.strip()

    'phone'
    def validate_phone(cls, v):
        if v and not v.replace('+', '').replace('-', '').replace(' ', '').replace('(', '').replace(')', '').isdigit():
            raise ValueError('Phone number must contain only digits and valid symbols')
        return v

    def dict(self, *args, **kwargs) -> Dict[str, Any]:
        kwargs["exclude_none"] = True
        return super().dict(*args, **kwargs)

    class Config:
        schema_extra = {
            "example": {
                "id": 12345,
                "username": "testuser",
                "firstName": "Test",
                "lastName": "User",
                "email": "test@example.com",
                "password": "password123",
                "phone": "+1234567890",
                "userStatus": 1
            }
        }
