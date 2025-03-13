from src.routers import (
    auth, user, table, reservation,
    category, product, cart, order,
)

routers = (
    auth.router,
    user.router,
    table.router,
    reservation.router,
    category.router,
    product.router,
    cart.router,
    order.router,
)
