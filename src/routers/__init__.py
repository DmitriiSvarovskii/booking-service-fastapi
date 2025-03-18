from src.routers import (
    auth, user, table, reservation,
    assortment, cart, order,
)

routers = (
    auth.router,
    user.router,
    table.router,
    reservation.router,
    assortment.router,
    cart.router,
    order.router,
)
