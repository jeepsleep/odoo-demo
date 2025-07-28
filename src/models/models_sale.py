from typing import Any, List, Optional

from pydantic import BaseModel, field_validator


class ProductRefModel(BaseModel):
    name: str


class SaleOrderLineModel(BaseModel):
    product_id: ProductRefModel
    product_uom_qty: float
    price_unit: Optional[float]  # Cambiado a Optional
    price_total: Optional[float] = None

class SaleOrderBaseModel(BaseModel):
    id: int
    partner_id: int
    date_order: str  # ISO format string
    order_line: List[SaleOrderLineModel]
    state: str = 'draft'

    @field_validator('state')
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Field cannot be empty')
        return v.strip()

class SaleOrderOutModel(SaleOrderBaseModel):
    name: str
    amount_total: Optional[float] = None
    user_id: Optional[Any] = None  
    partner_id: Optional[Any] = None 
    amount_untaxed: Optional[float] = None
    amount_tax: Optional[float] = None
    order_line: List[SaleOrderLineModel] = []

class SaleOrderListOutModel(BaseModel):
    orders: List[SaleOrderOutModel]
