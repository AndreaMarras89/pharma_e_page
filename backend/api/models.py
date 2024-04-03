"""Input&Output Intefaces definition"""

from typing import List

from pydantic import UUID4, BaseModel

class Product(BaseModel):
    """Model for Product"""

    id: str
    name: str
    price: float
    description: str
    image: str



#Lista Prodotti
class ProductListOutput(BaseModel):
    """Output model for search endpoint"""

    products: List[Product]