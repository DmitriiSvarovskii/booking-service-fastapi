# Общий шаблон для всех описаний
BASE_DESCRIPTION = """
{action} {item} текущего пользователя.

**Требования:**
- **JWT-токен** (если устарел — передать refresh token).
{extra_requirements}

**Возможные ошибки:**
- `401 Unauthorized` – Отсутствует или некорректный JWT-токен.
- `403 Forbidden` – Нет доступа.
- `500 Internal Server Error` – Внутренняя ошибка сервера.
"""

# Базовые параметры
PRODUCT_ID_REQUIREMENT = "- **product_id** (int) – ID товара, \
    который нужно {action}, передаётся в теле запроса (JSON)."
NO_EXTRA_REQUIREMENTS = ""

# Конкретные описания
REMOVE_ONE_ITEM_FROM_CART_SUMMARY = "Удаление одного товара из корзины"
REMOVE_ONE_ITEM_FROM_CART_DESCRIPTION = BASE_DESCRIPTION.format(
    action="Удаляет",
    item="один товар из корзины",
    extra_requirements=PRODUCT_ID_REQUIREMENT.format(action="удалить")
)

ADD_ONE_ITEM_FROM_CART_SUMMARY = "Добавление товара в корзину"
ADD_ONE_ITEM_FROM_CART_DESCRIPTION = BASE_DESCRIPTION.format(
    action="Добавляет",
    item="товар в корзину",
    extra_requirements=PRODUCT_ID_REQUIREMENT.format(action="добавить")
)

GET_ONE_ITEM_FROM_CART_SUMMARY = "Получение одного товара из корзины"
GET_ONE_ITEM_FROM_CART_DESCRIPTION = BASE_DESCRIPTION.format(
    action="Получает",
    item="один товар из корзины",
    extra_requirements=PRODUCT_ID_REQUIREMENT.format(action="получить")
)

GET_ALL_ITEMS_FROM_CART_SUMMARY = "Получение всех товаров из корзины"
GET_ALL_ITEMS_FROM_CART_DESCRIPTION = BASE_DESCRIPTION.format(
    action="Получает",
    item="все товары из корзины",
    extra_requirements=NO_EXTRA_REQUIREMENTS
)

DELETE_ALL_ITEMS_FROM_CART_SUMMARY = "Удаление всех товаров из корзины"
DELETE_ALL_ITEMS_FROM_CART_DESCRIPTION = BASE_DESCRIPTION.format(
    action="Удаляет",
    item="все товары из корзины",
    extra_requirements=NO_EXTRA_REQUIREMENTS
)
