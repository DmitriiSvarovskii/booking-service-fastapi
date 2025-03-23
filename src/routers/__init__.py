from fastapi import APIRouter, Depends
from src.dependencies.current_user import get_current_user

from src.routers import (
    auth, user, establishment, table, reservation,
    assortment, cart, order
)

# Создаем список роутеров, навешивая авторизацию глобально
routers = [
    APIRouter(
        prefix="/auth",
        dependencies=[Depends(get_current_user)],
        routes=auth.router.routes
    ),
    APIRouter(
        prefix="/user",
        dependencies=[Depends(get_current_user)],
        routes=user.router.routes
    ),
    APIRouter(
        prefix="/establishment",
        dependencies=[Depends(get_current_user)],
        routes=establishment.router.routes
    ),
    APIRouter(
        prefix="/table",
        dependencies=[Depends(get_current_user)],
        routes=table.router.routes
    ),
    APIRouter(
        prefix="/reservation",
        dependencies=[Depends(get_current_user)],
        routes=reservation.router.routes
    ),
    APIRouter(
        prefix="/assortment",
        dependencies=[Depends(get_current_user)],
        routes=assortment.router.routes
    ),
    APIRouter(
        prefix="/cart",
        dependencies=[Depends(get_current_user)],
        routes=cart.router.routes
    ),
    APIRouter(
        prefix="/order",
        dependencies=[Depends(get_current_user)],
        routes=order.router.routes
    ),
]
