# 🔧 Налаштування API

> **Навігація**: [README.md](README.md) ← [API_SETUP.md](API_SETUP.md) → [JOKE_FEATURE.md](JOKE_FEATURE.md)

## Швидке налаштування

### 1. Налаштування API URL

```bash
# В config.env файлі
JOKES_API_URL=https://your-api-domain.com/api/jokes/random

# Або через змінну середовища
export JOKES_API_URL=https://your-api-domain.com/api/jokes/random
```

### 2. Налаштування авторизації (опціонально)

```bash
# Якщо ваш API потребує авторизації
JOKES_API_KEY=your_api_key_here

# Або через змінну середовища
export JOKES_API_KEY=your_api_key_here
```

### 3. Налаштування таймауту (опціонально)

```bash
# Таймаут в секундах (за замовчуванням 10)
JOKES_API_TIMEOUT=15
```

## Підтримувані формати API відповідей

### Формат 1: Setup/Punchline
```json
{
  "id": 1,
  "setup": "Why don't scientists trust atoms?",
  "punchline": "Because they make up everything!",
  "type": "general"
}
```

### Формат 2: Question/Answer
```json
{
  "id": 2,
  "question": "Why do programmers prefer dark mode?",
  "answer": "Because light attracts bugs!",
  "category": "programming"
}
```

### Формат 3: Content
```json
{
  "id": 3,
  "title": "Funny Joke",
  "content": "Why did the chicken cross the road? To get to the other side!"
}
```

### Формат 4: Simple Text
```json
{
  "text": "Why don't eggs tell jokes? They'd crack each other up!"
}
```

## Тестування

### 1. Перевірка конфігурації

```bash
python test_joke.py
```

### 2. Тестування API вручну

```bash
# Перевірка доступності API
curl https://your-api-domain.com/api/jokes/random

# З авторизацією
curl -H "Authorization: Bearer your_api_key" \
     https://your-api-domain.com/api/jokes/random
```

### 3. Тестування в Docker

```bash
# Запуск з вашим API
docker run -d \
  --name telegram-bot \
  --secret bot_token \
  -e JOKES_API_URL="https://your-api-domain.com/api/jokes/random" \
  -e JOKES_API_KEY="your_api_key" \
  telegram-bot

# Перевірка логів
docker logs telegram-bot
```

## Обробка помилок

### HTTP статус коди

| Код | Опис | Обробка |
|-----|------|---------|
| 200 | Успіх | ✅ Відображається жарт |
| 401 | Неавторизований | ❌ Перевірте API ключ |
| 403 | Заборонено | ❌ Перевірте права доступу |
| 404 | Не знайдено | ❌ Перевірте URL |
| 500+ | Помилка сервера | ❌ Перевірте API |

### Логи помилок

```bash
# Перегляд логів
docker logs telegram-bot | grep -i joke

# Детальні логи
docker logs telegram-bot | grep -E "(joke|error|warning)"
```

## Приклади налаштування

### Локальний запуск

```bash
# 1. Налаштування
export JOKES_API_URL="https://your-api.com/jokes/random"
export JOKES_API_KEY="your_api_key"

# 2. Запуск
python main.py
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'
services:
  telegram-bot:
    build: .
    secrets:
      - bot_token
    environment:
      - JOKES_API_URL=https://your-api.com/jokes/random
      - JOKES_API_KEY=your_api_key
      - JOKES_API_TIMEOUT=15
    restart: unless-stopped

secrets:
  bot_token:
    external: true
```

### Docker Swarm

```bash
# Створення секрету для API ключа
echo "your_api_key" | docker secret create jokes_api_key -

# Запуск сервісу
docker service create \
  --name telegram-bot \
  --secret bot_token \
  --secret jokes_api_key \
  --env JOKES_API_URL="https://your-api.com/jokes/random" \
  --env JOKES_API_TIMEOUT=15 \
  telegram-bot
```

## Troubleshooting

### Проблема: API недоступний

```bash
# Перевірка доступності
curl -I https://your-api-domain.com/api/jokes/random

# Перевірка DNS
nslookup your-api-domain.com
```

### Проблема: 401 Unauthorized

```bash
# Перевірка API ключа
curl -H "Authorization: Bearer your_api_key" \
     https://your-api-domain.com/api/jokes/random
```

### Проблема: 404 Not Found

```bash
# Перевірка URL
curl https://your-api-domain.com/api/jokes/random

# Перевірка документації API
```

### Проблема: Таймаут

```bash
# Збільшення таймауту
export JOKES_API_TIMEOUT=30

# Перевірка швидкості API
time curl https://your-api-domain.com/api/jokes/random
```

## Моніторинг

### Перевірка статусу

```bash
# Статус контейнера
docker ps | grep telegram-bot

# Логи в реальному часі
docker logs -f telegram-bot

# Використання ресурсів
docker stats telegram-bot
```

### Метрики API

```bash
# Кількість запитів до API
docker logs telegram-bot | grep "Successfully fetched joke" | wc -l

# Помилки API
docker logs telegram-bot | grep "Jokes API" | grep -i error
```

## Безпека

### Рекомендації

1. **HTTPS**: Використовуйте тільки HTTPS для API
2. **API ключі**: Зберігайте в Docker secrets
3. **Таймаути**: Встановлюйте розумні таймаути
4. **Логування**: Не логуйте API ключі

### Безпечне налаштування

```bash
# Створення секрету
echo "your_api_key" | docker secret create jokes_api_key -

# Запуск з секретом
docker run -d \
  --name telegram-bot \
  --secret bot_token \
  --secret jokes_api_key \
  -e JOKES_API_URL="https://your-api.com/jokes/random" \
  telegram-bot
```

## Розширення

### Додавання нових API

1. Оновіть `JOKES_API_URL` в конфігурації
2. Адаптуйте `format_joke()` для нового формату
3. Додайте обробку специфічних помилок

### Додавання кешування

```python
import redis
from functools import lru_cache

@lru_cache(maxsize=100)
async def get_cached_joke():
    return await fetch_joke()
```

### Додавання категорій жартів

```python
async def get_joke_by_category(category: str):
    url = f"{Config.JOKES_API_URL}?category={category}"
    # Implementation
```

## Посилання

- **Швидкий старт**: [QUICK_START.md](QUICK_START.md)
- **Joke функціонал**: [JOKE_FEATURE.md](JOKE_FEATURE.md)
- **Головна документація**: [README.md](README.md)

---

**API налаштовано і готово до використання! 🚀**
