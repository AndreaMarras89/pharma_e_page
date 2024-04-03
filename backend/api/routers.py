"""Endpoint Definition"""

from backend.db.utils import DatabaseSessionMaker
from fastapi import APIRouter, HTTPException

from backend.db.tables import Product as ProductTable
from backend.api.models import Product, ProductListOutput, ProductDetailsInput, ProductDetailsOutput
from sqlalchemy import select


session_maker = DatabaseSessionMaker()

router = APIRouter()

@router.get("/products_list")
async def product_list() -> ProductListOutput:
    try:
        async with session_maker.get_session() as session:
            my_sql = select(ProductTable)
            result = await session.execute(my_sql)
            records = result.fetchall()
            product_list = []
            if records and len(records) > 0:
                for record in records:
                    product_list.append(Product(id = str(record[0].id), name = record[0].name, price = record[0].price, description = record[0].description, image = record[0].image))
        return ProductListOutput(products = product_list)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
    
    
@router.post("/product_details")
async def product_details(payload: ProductDetailsInput) -> ProductDetailsOutput:
    """Logic of the product_details endpoint"""

    try:
        async with session_maker.get_session() as session:
            my_sql = select(ProductTable).where(ProductTable.id == payload.product_id)
            result = await session.execute(my_sql)
            record = result.first()
            if record and len(record) > 0:
                return ProductDetailsOutput(
                    product_name=record[0].name,
                    product_description=record[0].description,
                    product_price=record[0].price,
                    product_image=record[0].image
                )
            else:
                raise HTTPException(
                    status_code=404,
                    detail=f"product with ID {payload.product_id} not found",
                )
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))