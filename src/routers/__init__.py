from src.routers import (
    auth, table, reservation,
    category, product, cart, order,
)

routers = (
    auth.router,
    table.router,
    reservation.router,
    category.router,
    product.router,
    cart.router,
    order.router,
)
