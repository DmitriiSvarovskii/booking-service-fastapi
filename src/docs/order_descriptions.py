BASE_DESCRIPTION = """
{action} {item} текущего пользователя.

**Требования:**
- **JWT-токен** (если устарел — передать refresh token).
{extra_requirements}

**Возможные ошибки:**
- `401 Unauthorized` – Отсутствует или некорректный JWT-токен.
- `403 Forbidden` – Нет доступа.
- `404 Not Found` – Не найдено.
- `500 Internal Server Error` – Внутренняя ошибка сервера.
"""

ORDER_ID_REQUIREMENT = "- **order_id** (int) – ID заказа, который нужно \
    {action}, передаётся в URL."

GET_ALL_ORDERS_SUMMARY = "Получение всех оформленных заказов"
GET_ALL_ORDERS_DESCRIPTION = BASE_DESCRIPTION.format(
    action="Получает",
    item="все оформленные заказы",
    extra_requirements="")

GET_ORDER_BY_ID_SUMMARY = "Получение одного заказа"
GET_ORDER_BY_ID_DESCRIPTION = BASE_DESCRIPTION.format(
    action="Получает",
    item="конкретный заказ",
    extra_requirements=ORDER_ID_REQUIREMENT.format(action="получить")
)

CREATE_ORDER_SUMMARY = "Создание нового заказа"
CREATE_ORDER_DESCRIPTION = BASE_DESCRIPTION.format(
    action="Создаёт",
    item="новый заказ",
    extra_requirements="- **order_data** (JSON) – Данные для создания заказа, \
        передаются в теле запроса."
)
