"""Endpoint Definition"""

from backend.db.utils import DatabaseSessionMaker
from fastapi import APIRouter, HTTPException

from backend.db.tables import Product as ProductTable, User, UserCart
from backend.api.models import Product, ProductListOutput, ProductDetailsInput, ProductDetailsOutput, ProductAddCartInput, ProductAddCartOutput, ProductRemovalAllInput, ProductRemovalAllOutput
from sqlalchemy import select, and_, insert, update, delete


session_maker = DatabaseSessionMaker()

router = APIRouter()


async def check_user_exists(user_id: str) -> bool:
    """Utility function to check if the user_id exists in the database"""

    async with session_maker.get_session() as session:
        my_query = select(User).where(user_id == User.uid)
        result = await session.execute(my_query)
        return_value = result.first()
        if return_value and len(return_value) > 0:
            return True
        return False


async def check_product_exists(product_id: str) -> bool:
    """Utility function to check if the product_id exists in the database"""

    async with session_maker.get_session() as session:
        my_query = select(ProductTable.id).where(ProductTable.id == product_id)
        result = await session.execute(my_query)
        return_value = result.first()
        if return_value and len(return_value) > 0:
            return True
        return False


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
    

@router.post("/add_product")
async def add_to_cart(payload: ProductAddCartInput) -> ProductAddCartOutput:
    """Logic of the add_product endpoint"""

    try:
        async with session_maker.get_session() as session:
            if await check_user_exists(payload.user_id) and await check_product_exists(
                payload.product_id
            ):
                my_sql = select(UserCart).where(
                    and_(
                        UserCart.user_id == payload.user_id,
                        UserCart.product_id == payload.product_id,
                    )
                )
                result = await session.execute(my_sql)
                record = result.first()
                if record and len(record) > 0:
                    my_sql = (
                        update(UserCart)
                        .where(
                            and_(
                                UserCart.product_id == payload.product_id,
                                UserCart.user_id == payload.user_id,
                            )
                        )
                        .values(quantity=record[0].quantity + payload.quantity)
                    )
                    compile = my_sql.compile()
                    result = await session.execute(my_sql)
                    await session.commit()
                else:
                    my_query = insert(UserCart).values(
                        product_id=payload.product_id,
                        user_id=payload.user_id,
                        quantity=payload.quantity,
                    )
                    compile = my_query.compile()
                    result = await session.execute(my_query)
                    await session.commit()
            else:
                raise HTTPException(
                    status_code=404,
                    detail=f"Product ID or UserID not found in the database",
                )
        return ProductAddCartOutput(added=True)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
    

@router.post("/product_removal_all")
async def product_removal_all(
    payload: ProductRemovalAllInput,
) -> ProductRemovalAllOutput:
    """Logic of the product_removal_all endpoint"""

    try:
        if not check_user_exists(payload.user_id):
            raise HTTPException(status_code=404, detail="User not found")

        async with session_maker.get_session() as session:
            my_sql = delete(UserCart).where(UserCart.user_id == payload.user_id)
            compile = my_sql.compile()
            result = await session.execute(my_sql)
            await session.commit()
            return ProductRemovalAllOutput(removed=True)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))