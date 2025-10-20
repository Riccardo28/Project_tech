from pydantic import BaseModel, Field
from typing import Optional


class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Item name")
    description: Optional[str] = Field(None, max_length=500, description="Item description")
    price: float = Field(..., gt=0, description="Item price (must be greater than 0)")
    is_available: bool = Field(True, description="Item availability status")


class ItemCreate(ItemBase):
    """Schema for creating a new item"""
    pass


class ItemUpdate(BaseModel):
    """Schema for updating an item (all fields optional)"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, gt=0)
    is_available: Optional[bool] = None


class Item(ItemBase):
    """Schema for item response"""
    id: int

    class Config:
        from_attributes = True
