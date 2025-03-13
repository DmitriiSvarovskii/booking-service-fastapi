import hmac
import hashlib
import json


def validate_webapp_data(init_data, bot_token):
    """
    Функция для проверки валидности данных, полученных через WebApp.

    :param init_data: Объект с данными WebApp (словарь).
    :param bot_token: Токен бота.
    :return: True, если данные валидны, иначе False.
    """

    # Получаем строку проверки (data_check_string)
    fields = [
        ("auth_date", init_data["auth_date"]),
        ("query_id", init_data["query_id"]),
        ("user", init_data["user"]),
    ]

    # Сортируем поля по имени ключа (алфавитно)
    fields_sorted = sorted(fields, key=lambda x: x[0])

    # Формируем строку для проверки
    data_check_string = "\n".join(
        f"{key}={value}" for key, value in fields_sorted) + "\n"

    # Генерация секретного ключа для HMAC
    secret_key = hmac.new(bot_token.encode(
        'utf-8'), "WebAppData".encode('utf-8'), hashlib.sha256).digest()

    # Вычисляем HMAC-SHA256 хеш для строки проверки
    generated_hash = hmac.new(secret_key, data_check_string.encode(
        'utf-8'), hashlib.sha256).hexdigest()

    # Сравниваем полученный хеш с тем, что пришел
    if generated_hash == init_data["hash"]:
        return True  # Данные валидны
    else:
        return False  # Данные невалидны


# Пример данных (init_data)
init_data = {
    "auth_date": 1696961678,
    "query_id": "AAGVbSskAAAAAJVtKyQX6XyE",
    "user": '{"id":606825877,"first_name":"Дмитрий","last_name":"Сваровский","username":"swarovskidima","language_code":"ru","is_premium":true,"allows_write_to_pm":true}',
    "hash": "b0c8bb03576e9ecf85171fe151bee2f996dec619353ce4a2bce72d6337f24678"
}
# # Пример данных (init_data)
# init_data = {
#     "auth_date": 1741873665,
#     "query_id": "AAGVbSskAAAAAJVtKyRKPkaF",
#     "user": '{"id":606825877,"first_name":"Дмитрий","last_name":"Сваровский","username":"swarovskidima","language_code":"ru","allows_write_to_pm":true,"photo_url":"https://t.me/i/userpic/320/rSGM8ZYqLcQ8KuQ4MlqAXlf2OQLeJztVZpj5KBtpgno.svg"}',
#     "hash": "9a14d10feaf6a56730a801c70f27635206d460f51748411002ad16ab7e6972c0"
# }

# Пример токена бота
bot_token = '6141111072:AAH8CBhf7iQUVNFCjR_STaBf9h_mYHSggvo'
# bot_token = '7819818690:AAEHWwWzxGo9ENY2uvyjrgBpD-5F8FQhalc'

# Проверка данных
is_valid = validate_webapp_data(init_data, bot_token)

if is_valid:
    print("Данные валидны: True")
else:
    print("Данные валидны: False")
