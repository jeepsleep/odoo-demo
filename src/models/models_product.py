from typing import List, Optional, Union

from pydantic import BaseModel


class NestedNameModel(BaseModel):
    name: str

class ProductBaseModel(BaseModel):
    id: int
    name: str
    create_date: Optional[str]
    default_code: Optional[str]
    type: Optional[str]
    categ_id: Optional[NestedNameModel]
    uom_id: Optional[NestedNameModel]
    uom_po_id: Optional[Union[int, NestedNameModel]]  # permite int o dict
    list_price: Optional[float]
    standard_price: Optional[float]
    description_sale: Optional[str]

class ProductOutModel(ProductBaseModel):
    id: int

class ProductListOutModel(BaseModel):
    products: List[ProductOutModel]
