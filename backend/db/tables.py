"""Definition of the tables"""

from sqlalchemy import UUID, Column, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Product(Base):
    """Product Table"""

    __tablename__ = "Products"

    id = Column("ID", UUID, primary_key=True)
    name = Column("Name", String)
    price = Column("Price", Float)
    description = Column("Description", Text)
    quantity = Column("Quantity", Integer)
    image = Column("Image", String)


class User(Base):
    """User Table"""

    __tablename__ = "Users"

    uid = Column("ID", UUID, primary_key=True)
    username = Column("Username", String)
    password = Column("Pass", String)


class UserCart(Base):
    """UserCart Table"""

    __tablename__ = "User_Cart"

    user_id = Column("ID_user", UUID, primary_key=True)
    product_id = Column("ID_product", UUID, primary_key=True)
    quantity = Column("Quantity", Integer)


class Orders(Base):
    """Order Table"""

    __tablename__ = "Orders"

    order_id = Column("ID_order", UUID, primary_key=True)
    user_id = Column("ID_user", UUID)
    product_id = Column("ID_product", UUID)
    quantity = Column("Quantity", Integer)
    time = Column("Date", DateTime)


class UserDataInvoicing(Base):
    """User Data Invoicing Table"""

    __tablename__ = "User_Data_Invoicing"

    user_ID = Column("User_ID", UUID, primary_key=True)
    name = Column("Name", String)
    last_name = Column("Last_Name", String)
    cf = Column("CF", String)
    address = Column("Address", String)
    billing_address = Column("Billing_Address", String)
