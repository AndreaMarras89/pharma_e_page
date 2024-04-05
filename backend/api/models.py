"""Input&Output Intefaces definition"""

from datetime import datetime
from typing import List

from pydantic import UUID4, BaseModel


class Product(BaseModel):
    """Model for Product"""

    id: str
    name: str
    price: float
    description: str
    image: str
    icon: str


class ProductInCart(Product):
    """Extension of the Product for the cart"""

    quantity: int


class UserOrder(BaseModel):
    """class for the order of the user"""

    order_id: UUID4
    date: datetime


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
    quantity: int
    product_icon: str


class ProductRemovalAllInput(BaseModel):
    """Input model for product_removal_all endpoint"""

    user_id: UUID4


class ProductRemovalAllOutput(BaseModel):
    """Output model for product_removal_all endpoint"""

    removed: bool


class InfoInvoicingInput(BaseModel):
    """Input model for the info about the invoice"""

    user_ID: UUID4
    name: str
    last_name: str
    cf: str
    address: str
    billing_address: str


class InfoInvoicingOutput(BaseModel):
    """Output model for the info about the invoice"""

    success: bool


class OrderCreationInput(BaseModel):
    """Input for the creation of the order"""

    user_ID: UUID4


class OrderCreationOutput(BaseModel):
    """Output for the creation of the order"""

    order_id: UUID4


class CartListInput(BaseModel):
    """Input for the cart list"""

    user_id: UUID4


class CartListOutput(BaseModel):
    """The output of the cart"""

    products: list[ProductInCart]


class OrderUserHistoryInput(BaseModel):
    """Input of the history of the orders made by the user"""

    user_id: UUID4


class OrderUserHistoryOutput(BaseModel):
    """Output of the history of the orders made by the user"""

    orders_list: list[UserOrder]
