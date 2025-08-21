# Используем официальный Python образ
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл с зависимостями
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код приложения
COPY src/ ./src/

# Устанавливаем переменную окружения для Python
ENV PYTHONPATH=/app

# Открываем порт
EXPOSE 8080

# Команда для запуска приложения
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
