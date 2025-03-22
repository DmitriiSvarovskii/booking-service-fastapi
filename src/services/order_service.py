from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.cart import CartRepository
from src.repositories.order import OrderRepository
from src.schemas.order import OrderCreate, OrderDetailsCreate
from src.schemas.cart import CartAllGet


class OrderService:
    @staticmethod
    async def create_order_from_cart(
        order_data: OrderCreate,
        session: AsyncSession
    ) -> dict:
        user_id = order_data.user_id
        cart_items = await CartRepository.get_cart_items(
            user_id=user_id,
            session=session
        )

        if not cart_items:
            return {"status": "error", "message": "Cart is empty"}

        total_price = sum(float(item.product.price *
                          item.quantity) for item in cart_items)
        order_data.total_price = total_price

        order_id = await OrderRepository.create_order(
            order_data=order_data,
            session=session
        )

        order_details_list = OrderService._generate_order_details(
            order_id, cart_items)

        await OrderRepository.create_order_details(
            order_details_list,
            session
        )

        await CartRepository.remove_all_from_cart_by_user_id(user_id, session)

        return {"status": "success", "order_id": order_id}

    @staticmethod
    def _generate_order_details(
        order_id: int,
        cart_items: list[CartAllGet]
    ) -> list[OrderDetailsCreate]:
        """Создаёт список объектов OrderDetailsCreate из cart_items"""
        return [
            OrderDetailsCreate(
                order_id=order_id,
                product_id=item.product_id,
                quantity=item.quantity
            ) for item in cart_items
        ]
