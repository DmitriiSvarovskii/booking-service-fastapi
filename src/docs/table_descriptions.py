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

TABLE_ID_REQUIREMENT = "- **table_id** (int) – ID стола, который нужно \
    {action}, передаётся в URL."

GET_ALL_TABLES_SUMMARY = "Получение всех столов"
GET_ALL_TABLES_DESCRIPTION = BASE_DESCRIPTION.format(
    action="Получает",
    item="все столы",
    extra_requirements="")

GET_TABLE_BY_ID_SUMMARY = "Получение одного стола"
GET_TABLE_BY_ID_DESCRIPTION = BASE_DESCRIPTION.format(
    action="Получает",
    item="конкретный стол",
    extra_requirements=TABLE_ID_REQUIREMENT.format(action="получить")
)
