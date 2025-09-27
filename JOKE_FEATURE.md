# 🎭 Joke Feature

> **Навігація**: [README.md](README.md) ← [JOKE_FEATURE.md](JOKE_FEATURE.md) → [API_SETUP.md](API_SETUP.md)

## Огляд

Команда `/joke` додає функціональність отримання випадкових жартів з вашого власного HTTP API до Telegram бота.

## Функціональність

### Команди
- `/joke` - Отримати випадковий жарт з вашого API

### Кнопки
- **🎭 Joke** - В головному меню для швидкого доступу
- **🎭 Another Joke** - Для отримання нового жарту
- **🔄 Try Again** - При помилці завантаження

## API

### Ваше HTTP API
- **URL**: Налаштовується через `JOKES_API_URL`
- **Endpoint**: Налаштовується через `JOKES_API_ENDPOINT` (за замовчуванням `/api/getJoke`)
- **Метод**: POST
- **Timeout**: 10 секунд (налаштовується)
- **Авторизація**: Bearer token (опціонально)
- **Формат запиту**: JSON
- **Формат відповіді**: JSON

### API Schema

#### Запит (Request)
```json
{
  "input": "Розкажи анекдот"
}
```

**Поля запиту:**
- `input` (string, nullable) - Будь-який текстовий ввід. Зміст ігнорується моделлю, але поле обов'язкове.

#### Відповідь (Response)
```json
{
  "response": "Чому програмісти плутають Хелловін та Різдво? Тому що 31 OCT = 25 DEC."
}
```

**Поля відповіді:**
- `response` (string, nullable) - Згенерований текст жарту.

### HTTP статус коди

| Код | Опис | Обробка |
|-----|------|---------|
| 200 | Успіх | ✅ Відображається жарт |
| 401 | Неавторизований | ❌ Перевірте API ключ |
| 403 | Заборонено | ❌ Перевірте права доступу |
| 404 | Не знайдено | ❌ Перевірте URL та endpoint |
| 500 | Помилка сервера | ❌ Перевірте API |

## Конфігурація

### Змінні середовища

| Змінна | Опис | Обов'язкова | За замовчуванням |
|--------|------|-------------|------------------|
| `JOKES_API_URL` | Базовий URL вашого API | ✅ | - |
| `JOKES_API_ENDPOINT` | Endpoint для отримання жартів | ❌ | `/api/getJoke` |
| `JOKES_API_TIMEOUT` | Таймаут запиту (секунди) | ❌ | `10` |
| `JOKES_API_KEY` | API ключ для авторизації | ❌ | - |

### Приклад налаштування

```bash
# config.env
JOKES_API_URL=https://your-api-domain.com
JOKES_API_ENDPOINT=/api/getJoke
JOKES_API_TIMEOUT=15
JOKES_API_KEY=your_api_key_here
```

### Docker налаштування

```bash
# Запуск з вашим API
docker run -d \
  --name telegram-bot \
  -e BOT_TOKEN="YOUR_BOT_TOKEN" \
  -e JOKES_API_URL="https://your-api-domain.com" \
  -e JOKES_API_ENDPOINT="/api/getJoke" \
  -e JOKES_API_KEY="your_api_key" \
  -e JOKES_API_TIMEOUT=15 \
  telegram-bot
```

## Архітектура

### Модулі

#### `utils.py`
- `fetch_joke()` - Асинхронне отримання жарту з API
- `format_joke()` - Форматування жарту для відображення
- `get_random_joke()` - Головна функція для отримання жарту

#### `handlers/command_handlers.py`
- `joke_command()` - Обробник команди `/joke`

#### `handlers/callback_handlers.py`
- `handle_joke_callback()` - Обробник кнопки жарту
- Додана кнопка "🎭 Joke" в головне меню

#### `config.py`
- `JOKES_API_URL` - URL API
- `JOKES_API_TIMEOUT` - Таймаут
- `JOKES_API_KEY` - API ключ

## Використання

### Локальний запуск

```bash
# 1. Встановлення залежностей
pip install -r requirements.txt

# 2. Налаштування (опціонально)
export JOKES_API_URL="https://your-jokes-api.com/random"
export JOKES_API_TIMEOUT=15

# 3. Запуск
python main.py
```

### Docker

```bash
# Запуск з налаштуваннями
docker run -d \
  --name telegram-bot \
  -e BOT_TOKEN="YOUR_BOT_TOKEN" \
  -e JOKES_API_URL="https://your-jokes-api.com/random" \
  -e JOKES_API_TIMEOUT=15 \
  telegram-bot
```

## Обробка помилок

### Типи помилок

1. **Timeout** - API не відповідає вчасно
2. **Connection Error** - Проблеми з мережею
3. **Invalid Response** - Невірний формат відповіді
4. **API Error** - Помилка API (4xx, 5xx)

### Обробка помилок

```python
try:
    joke_data = await fetch_joke()
    if joke_data:
        formatted_joke = format_joke(joke_data)
    else:
        # Fallback message
        formatted_joke = "😅 Sorry, I couldn't fetch a joke right now. Try again later!"
except Exception as e:
    logger.error(f"Error fetching joke: {e}")
    # Error handling
```

## Тестування

### Тестовий скрипт

```bash
# Запуск тестів
python test_joke.py
```

### Тестовий приклад

```python
import asyncio
from utils import get_random_joke

async def test():
    joke = await get_random_joke()
    print(joke)

asyncio.run(test())
```

## Логування

### Рівні логування

- **INFO**: Успішне отримання жарту
- **WARNING**: API повернув неочікуваний статус
- **ERROR**: Помилки мережі, таймаути, неочікувані помилки

### Приклад логів

```
2024-01-15 10:30:15 - utils - INFO - Successfully fetched joke from custom API: 123
2024-01-15 10:30:20 - utils - ERROR - Jokes API request timed out
2024-01-15 10:30:25 - utils - WARNING - Jokes API returned status 500
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

## Безпека

### Рекомендації

1. **API ключі**: Зберігайте в змінних середовища
2. **Таймаути**: Встановлюйте розумні таймаути
3. **Валідація**: Перевіряйте відповіді API
4. **Логування**: Не логуйте чутливі дані

### Приклад безпечної конфігурації

```bash
# Змінні середовища
export JOKES_API_KEY="your_api_key"

# Docker run
docker run -d \
  --name telegram-bot \
  -e BOT_TOKEN="YOUR_BOT_TOKEN" \
  -e JOKES_API_KEY="your_api_key" \
  telegram-bot
```

## Моніторинг

### Метрики

- Кількість запитів до API
- Час відповіді API
- Кількість помилок
- Популярність команди `/joke`

### Health Check

```python
async def health_check():
    try:
        joke = await fetch_joke()
        return joke is not None
    except:
        return False
```

## Troubleshooting

### Часті проблеми

1. **API недоступний**
   - Перевірте URL
   - Перевірте мережеве з'єднання
   - Перевірте таймаут

2. **Невірний формат відповіді**
   - Перевірте API документацію
   - Оновіть `format_joke()`

3. **Повільна робота**
   - Зменшіть таймаут
   - Додайте кешування
   - Використовуйте асинхронні запити

### Діагностика

```bash
# Перевірка API
curl https://your-api-domain.com/api/jokes/random

# Тест функцій
python test_joke.py

# Логи
docker logs telegram-bot | grep joke
```

## Посилання

- **Швидкий старт**: [QUICK_START.md](QUICK_START.md)
- **Налаштування API**: [API_SETUP.md](API_SETUP.md)
- **Головна документація**: [README.md](README.md)

---

**Joke функціонал готовий до використання! 🎉**