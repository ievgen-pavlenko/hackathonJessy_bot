# Використовуємо офіційний Python образ
FROM python:3.11-slim

# Встановлюємо робочу директорію
WORKDIR /app

# Встановлюємо системні залежності
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копіюємо файли залежностей
COPY requirements.txt .

# Встановлюємо Python залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо код додатку
COPY . .

# Створюємо користувача для безпеки
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

# Відкриваємо порт (якщо потрібно для моніторингу)
EXPOSE 8000

# Встановлюємо змінні середовища за замовчуванням
ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL=INFO

# Команда запуску
CMD ["python", "main.py"]
