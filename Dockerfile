# Используем официальный образ Python
FROM python:3.11

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY req.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r req.txt

# Копируем код приложения
COPY . .

# Открываем порт для FastAPI
EXPOSE 8000

# Запускаем приложение
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]