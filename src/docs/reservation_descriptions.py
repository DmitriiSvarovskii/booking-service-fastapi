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

RESERVATION_ID_REQUIREMENT = "- **reservation_id** (int) – ID бронирования, \
    который нужно {action}, передаётся в URL."

GET_ALL_RESERVATIONS_SUMMARY = "Получение всех бронирований"
GET_ALL_RESERVATIONS_DESCRIPTION = BASE_DESCRIPTION.format(
    action="Получает",
    item="все бронирования",
    extra_requirements="")

GET_RESERVATION_BY_ID_SUMMARY = "Получение одного бронирования"
GET_RESERVATION_BY_ID_DESCRIPTION = BASE_DESCRIPTION.format(
    action="Получает",
    item="конкретное бронирование",
    extra_requirements=RESERVATION_ID_REQUIREMENT.format(action="получить")
)

CREATE_RESERVATION_SUMMARY = "Создание нового бронирования"
CREATE_RESERVATION_DESCRIPTION = BASE_DESCRIPTION.format(
    action="Создаёт",
    item="новое бронирование",
    extra_requirements="- **reservation_data** (JSON) – Данные для создания \
        бронирования, передаются в теле запроса."
)
