from src.routers import table
from src.routers import booking
from src.routers import category
from src.routers import product
from src.routers import cart
from src.routers import order

routers = (
    table.router,
    booking.router,
    category.router,
    product.router,
    cart.router,
    order.router,
)
