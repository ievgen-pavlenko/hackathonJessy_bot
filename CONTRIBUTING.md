# 🤝 Внесок до проекту

Дякуємо за ваш інтерес до внеску в Telegram Bot! Цей документ містить інструкції для внеску в проект.

## 📋 Зміст

- [Код поведінки](#код-поведінки)
- [Як внести свій внесок](#як-внести-свій-внесок)
- [Процес розробки](#процес-розробки)
- [Стандарти коду](#стандарти-коду)
- [Тестування](#тестування)
- [Документація](#документація)

## Код поведінки

### Наші зобов'язання

Ми зобов'язуємося зробити участь у нашому проекті комфортним досвідом для всіх, незалежно від віку, розміру тіла, видимої або невидимої інвалідності, етнічної приналежності, статі, гендерної ідентичності та вираження, рівня досвіду, освіти, соціально-економічного статусу, національності, зовнішності, раси, релігії або сексуальної ідентичності та орієнтації.

### Очікувана поведінка

- Використання привітливої та інклюзивної мови
- Повага до різних точок зору та досвіду
- Прийняття конструктивної критики
- Фокус на тому, що найкраще для спільноти
- Емпатія до інших учасників спільноти

### Неприйнятна поведінка

- Використання сексуалізованої мови або образів
- Тролінг, образливі/принизливі коментарі або особисті атаки
- Публічні або приватні домагання
- Публікація приватної інформації без дозволу
- Інша поведінка, яка може бути розцінена як неприйнятна в професійному середовищі

## Як внести свій внесок

### Звіти про помилки

Використовуйте GitHub Issues для звітів про помилки. Будь ласка, включіть:

- **Короткий опис** проблеми
- **Кроки для відтворення** проблеми
- **Очікувану поведінку**
- **Фактичну поведінку**
- **Скріншоти** (якщо застосовно)
- **Версію** Python, Docker, операційної системи
- **Логи** (якщо застосовно)

### Запити функцій

Ми вітаємо ідеї для нових функцій! Створіть issue з:

- **Описом** нової функції
- **Обґрунтуванням** чому це корисно
- **Прикладами** використання
- **Можливими** реалізаціями

### Pull Requests

1. **Fork** репозиторій
2. **Створіть** feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** зміни (`git commit -m 'Add amazing feature'`)
4. **Push** в branch (`git push origin feature/amazing-feature`)
5. **Створіть** Pull Request

## Процес розробки

### Налаштування середовища розробки

```bash
# 1. Клонування репозиторію
git clone https://github.com/yourusername/telegram-bot.git
cd telegram-bot

# 2. Створення віртуального середовища
python -m venv venv
source venv/bin/activate  # Linux/Mac
# або
venv\Scripts\activate     # Windows

# 3. Встановлення залежностей
pip install -r requirements.txt

# 4. Встановлення dev залежностей
pip install pytest black flake8 mypy

# 5. Налаштування pre-commit hooks
pre-commit install
```

### Структура проекту

```
telegram-bot/
├── handlers/              # Обробники подій
│   ├── command_handlers.py
│   ├── message_handlers.py
│   ├── callback_handlers.py
│   └── error_handlers.py
├── main.py               # Точка входу
├── config.py             # Конфігурація
├── utils.py              # Допоміжні функції
├── tests/                # Тести
├── docs/                 # Документація
└── requirements.txt      # Залежності
```

## Стандарти коду

### Python

- **PEP 8** - стиль коду
- **Type hints** - анотації типів
- **Docstrings** - документація функцій
- **Логування** - використання logging модуля

### Приклад коду

```python
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

async def fetch_joke() -> Optional[Dict[str, Any]]:
    """
    Fetch a random joke from the API.
    
    Returns:
        Optional[Dict[str, Any]]: Joke data or None if failed
    """
    try:
        # Implementation here
        logger.info("Successfully fetched joke")
        return joke_data
    except Exception as e:
        logger.error(f"Error fetching joke: {e}")
        return None
```

### Форматування коду

```bash
# Автоматичне форматування
black .

# Перевірка стилю
flake8 .

# Перевірка типів
mypy .
```

## Тестування

### Запуск тестів

```bash
# Всі тести
pytest

# З покриттям
pytest --cov=.

# Конкретний тест
pytest tests/test_handlers.py::test_joke_command
```

### Написання тестів

```python
import pytest
from unittest.mock import AsyncMock, patch
from handlers.command_handlers import joke_command

@pytest.mark.asyncio
async def test_joke_command():
    """Test joke command handler."""
    # Setup
    update = AsyncMock()
    context = AsyncMock()
    
    # Mock API response
    with patch('utils.get_random_joke', return_value="Test joke"):
        await joke_command(update, context)
        
        # Assertions
        update.message.reply_text.assert_called_once()
```

### Покриття коду

```bash
# Генерація звіту покриття
pytest --cov=. --cov-report=html

# Перегляд звіту
open htmlcov/index.html
```

## Документація

### Оновлення документації

1. **README.md** - головна документація
2. **API_SETUP.md** - налаштування API
3. **JOKE_FEATURE.md** - функціонал жартів
4. **QUICK_START.md** - швидкий старт
5. **docker-examples.md** - Docker приклади

### Стандарти документації

- **Markdown** формат
- **Емодзі** для заголовків
- **Посилання** між файлами
- **Приклади коду** з підсвічуванням синтаксису
- **Структуровані** секції

### Приклад документації

```markdown
# 🎭 Joke Feature

> **Навігація**: [README.md](README.md) ← [JOKE_FEATURE.md](JOKE_FEATURE.md)

## Огляд

Команда `/joke` додає функціональність отримання випадкових жартів.

## Використання

```python
from utils import get_random_joke

joke = await get_random_joke()
print(joke)
```
```

## Процес рев'ю

### Для контрибуторів

1. **Створіть** feature branch
2. **Напишіть** тести для нової функції
3. **Оновіть** документацію
4. **Запустіть** тести та перевірки
5. **Створіть** Pull Request

### Для мейнтейнерів

1. **Перевірте** код на відповідність стандартам
2. **Запустіть** тести
3. **Перевірте** документацію
4. **Протестуйте** функціональність
5. **Approve** або запитайте зміни

## Зв'язок

- **GitHub Issues** - для звітів про помилки та запитів функцій
- **GitHub Discussions** - для загальних обговорень
- **Pull Requests** - для внесків коду

## Ліцензія

Вносячи внесок, ви погоджуєтесь, що ваш внесок буде ліцензований під MIT License.

## Дякуємо

Дякуємо за ваш внесок у Telegram Bot! 🎉

---

**Разом ми робимо Telegram Bot кращим! 🚀**
