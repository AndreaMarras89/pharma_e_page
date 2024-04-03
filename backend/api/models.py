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


class ProductListOutput(BaseModel):
    """Output model for search endpoint"""

    products: List[Product]
    
class ProductAddCartInput(BaseModel):
    """Input model for add_product endpoint"""

    user_id: UUID4
    product_id: UUID4
    quantity: int = 1


class ProductAddCartOutput(BaseModel):
    """Output model for add_product endpoint"""

    added: bool
    
class ProductDetailsInput(BaseModel):
    """Input model for product_details endpoint"""

    product_id: UUID4


class ProductDetailsOutput(BaseModel):
    """Output model for product_details endpoint"""

    product_name: str
    product_description: str
    product_price: float
    product_image: str