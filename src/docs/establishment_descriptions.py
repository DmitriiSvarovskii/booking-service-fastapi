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

ESTABLISHMENT_ID_REQUIREMENT = "- **establishment_id** (int) – ID заведения, \
    который нужно {action}, передаётся в URL."

GET_ALL_ESTABLISHMENTS_SUMMARY = "Получение всех заведений"
GET_ALL_ESTABLISHMENTS_DESCRIPTION = BASE_DESCRIPTION.format(
    action="Получает",
    item="все заведения",
    extra_requirements="")

GET_ESTABLISHMENT_BY_ID_SUMMARY = "Получение одного заведения"
GET_ESTABLISHMENT_BY_ID_DESCRIPTION = BASE_DESCRIPTION.format(
    action="Получает",
    item="конкретное заведение",
    extra_requirements=ESTABLISHMENT_ID_REQUIREMENT.format(action="получить")
)
