"""Endpoint Definition"""

from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, HTTPException
from sqlalchemy import and_, delete, insert, select, update

from backend.api.models import (CartListInput, CartListOutput,
                                InfoInvoicingInput, InfoInvoicingOutput,
                                OrderCreationInput, OrderCreationOutput,
                                OrderUserHistoryInput, OrderUserHistoryOutput,
                                Product, ProductAddCartInput,
                                ProductAddCartOutput, ProductDetailsInput,
                                ProductDetailsOutput, ProductInCart,
                                ProductListOutput, ProductRemovalAllInput,
                                ProductRemovalAllOutput, UserOrder)
from backend.db.tables import Orders
from backend.db.tables import Product as ProductTable
from backend.db.tables import User, UserCart, UserDataInvoicing
from backend.db.utils import DatabaseSessionMaker

router = APIRouter()
session_maker = DatabaseSessionMaker()


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
                    product_list.append(
                        Product(
                            id=str(record[0].id),
                            name=record[0].name,
                            price=record[0].price,
                            description=record[0].description,
                            image=record[0].image,
                        )
                    )
        return ProductListOutput(products=product_list)
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
                    quantity=record[0].quantity,
                    product_image=record[0].image,
                )
            else:
                raise HTTPException(
                    status_code=404,
                    detail=f"product with ID {payload.product_id} not found",
                )
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@router.post("/product_removal_all")
async def product_removal_all(
    payload: ProductRemovalAllInput,
) -> ProductRemovalAllOutput:
    """Logic of the product_removal_all endpoint"""

    try:
        if not await check_user_exists(payload.user_id):
            raise HTTPException(status_code=404, detail="User not found")

        async with session_maker.get_session() as session:
            my_sql = delete(UserCart).where(UserCart.user_id == payload.user_id)
            compile = my_sql.compile()
            result = await session.execute(my_sql)
            await session.commit()
            return ProductRemovalAllOutput(removed=True)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@router.post("/info_invoicing")
async def add_info_invoicing(payload: InfoInvoicingInput) -> InfoInvoicingOutput:
    try:
        async with session_maker.get_session() as session:
            my_query = insert(UserDataInvoicing).values(
                ID=str(uuid4()),
                user_ID=payload.user_ID,
                name=payload.name,
                last_name=payload.last_name,
                cf=payload.cf,
                address=payload.address,
                billing_address=payload.billing_address,
            )
            compile = my_query.compile()
            result = await session.execute(my_query)
            await session.commit()
            return InfoInvoicingOutput(success=True)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@router.post("/orders")
async def order_creation(payload: OrderCreationInput) -> OrderCreationOutput:
    try:
        products_to_add = []
        async with session_maker.get_session() as session:
            my_sql = select(UserCart).where(UserCart.user_id == payload.user_ID)
            result = await session.execute(my_sql)
            records = result.fetchall()
            if records and len(records) > 0:
                order_ID = str(uuid4())
                current_date = datetime.now()

                for record in records:
                    product = record[0].product_id
                    quantity = record[0].quantity
                    products_to_add.append((product, quantity))
            else:
                raise HTTPException(
                    status_code=404,
                    detail=f"user with ID {payload.user_ID} not found",
                )
        for product in products_to_add:

            my_sql = insert(Orders).values(
                order_id=order_ID,
                user_id=payload.user_ID,
                product_id=product[0],
                quantity=product[1],
                time=current_date,
            )
            async with session_maker.get_session() as session2:
                compile = my_sql.compile()
                result = await session2.execute(my_sql)
                await session2.commit()
                return OrderCreationOutput(order_id=order_ID)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@router.post("/cart_details")
async def cart_list_items(payload: CartListInput) -> CartListOutput:
    try:
        async with session_maker.get_session() as session:
            my_sql = select(UserCart).where(UserCart.user_id == payload.user_id)
            result = await session.execute(my_sql)
            records = result.fetchall()
            cart_products = []
            if records and len(records) > 0:
                for record in records:
                    my_query = select(ProductTable).where(
                        ProductTable.id == record[0].product_id
                    )
                    result = await session.execute(my_query)
                    product = result.first()
                    if product and len(product) > 0:
                        cart_products.append(
                            ProductInCart(
                                id=str(product[0].id),
                                name=product[0].name,
                                price=product[0].price,
                                description=product[0].description,
                                quantity=record[0].quantity,
                                image=product[0].image,
                            )
                        )
            return ProductListOutput(products=cart_products)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@router.post("/order_history")
async def order_history(payload: OrderUserHistoryInput) -> OrderUserHistoryOutput:
    try:
        async with session_maker.get_session() as session:
            my_sql = (
                select(Orders.order_id, Orders.time)
                .distinct()
                .where(Orders.user_id == payload.user_id)
            )
            result = await session.execute(my_sql)
            records = result.fetchall()
            order_history_list = []
            if records and len(records) > 0:
                for record in records:
                    print(record)
                    order_history_list.append(
                        UserOrder(order_id=record[0], date=record[1])
                    )
            return OrderUserHistoryOutput(orders_list=order_history_list)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
