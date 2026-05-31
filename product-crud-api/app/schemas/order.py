from pydantic import BaseModel
from typing import List
from datetime import datetime


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int
    
class OrderCreate(BaseModel):
    items: List[OrderItemCreate]
    
class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int 
    price: float
    
    class Config: 
        from_attributes = True
        
class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_price: float
    status: str
    transaction_ref: str | None
    created_at: datetime
    items: List[OrderItemResponse]
    
    class Config:
        from_attributes = True