from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class InventoryItemBase(BaseModel):
    name: str
    type: str
    serial_number: str
    status: Optional[str] = None
    daily_rate: float

class InventoryItemCreate(InventoryItemBase):
    pass

class InventoryItemRead(InventoryItemBase):
    id: int

    class Config:
        orm_mode = True

class ClientBase(BaseModel):
    name: str
    contact_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

class ClientCreate(ClientBase):
    pass

class ClientRead(ClientBase):
    id: int

    class Config:
        orm_mode = True

class JobBase(BaseModel):
    name: str
    client_id: int
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class JobCreate(JobBase):
    pass

class JobRead(JobBase):
    id: int

    class Config:
        orm_mode = True

class QuoteBase(BaseModel):
    job_id: int
    created_at: Optional[datetime] = None
    total_amount: float = 0

class QuoteCreate(QuoteBase):
    pass

class QuoteRead(QuoteBase):
    id: int

    class Config:
        orm_mode = True

class QuoteItemBase(BaseModel):
    quote_id: int
    inventory_item_id: int
    quantity: int
    price_per_day: float
    total_price: float

class QuoteItemCreate(QuoteItemBase):
    pass

class QuoteItemRead(QuoteItemBase):
    id: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None

class UserCreate(BaseModel):
    username: str
    password: str
