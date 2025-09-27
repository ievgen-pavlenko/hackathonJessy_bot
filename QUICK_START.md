# 🚀 Швидкий старт

> **Навігація**: [README.md](README.md) ← [QUICK_START.md](QUICK_START.md) → [API_SETUP.md](API_SETUP.md)

## ⚡ Мінімальний запуск

### Локально (30 секунд)

```bash
# 1. Клонування
git clone <repo-url> && cd telegram-bot

# 2. Встановлення
pip install -r requirements.txt

# 3. Налаштування
cp config.env .env
# Відредагуйте .env з вашим токеном

# 4. Запуск
python main.py
```

### Docker (1 хвилина)

```bash
# 1. Секрет
# BOT_TOKEN передається через змінну середовища

# 2. Збірка
docker build -t telegram-bot .

# 3. Запуск
docker run -d --name telegram-bot -e BOT_TOKEN="YOUR_BOT_TOKEN" telegram-bot
```

## 🔧 Швидкі команди

### Docker

```bash
# Збірка
docker build -t telegram-bot .

# Запуск
docker run -d --name telegram-bot -e BOT_TOKEN="YOUR_BOT_TOKEN" telegram-bot

# Логи
docker logs -f telegram-bot

# Зупинка
docker stop telegram-bot && docker rm telegram-bot
```

### Docker Compose

```bash
# Запуск
docker-compose up -d

# Логи
docker-compose logs -f

# Зупинка
docker-compose down
```

### Docker Swarm

```bash
# Ініціалізація
docker swarm init

# Секрет
# BOT_TOKEN передається через змінну середовища

# Сервіс
docker service create --name telegram-bot -e BOT_TOKEN="YOUR_BOT_TOKEN" telegram-bot

# Масштабування
docker service scale telegram-bot=3
```

## 🐛 Швидке налагодження

```bash
# Перевірка статусу
docker ps | grep telegram-bot

# Логи
docker logs telegram-bot

# Вхід в контейнер
docker exec -it telegram-bot bash

# Перевірка змінних
docker exec telegram-bot env | grep BOT

# Перевірка секрету
docker exec telegram-bot printenv BOT_TOKEN
```

## 📊 Моніторинг

```bash
# Ресурси
docker stats telegram-bot

# Деталі
docker inspect telegram-bot

# Сервіси (Swarm)
docker service ls
docker service ps telegram-bot
```

## 🔄 Оновлення

```bash
# Перебудова
docker build -t telegram-bot .

# Перезапуск
docker restart telegram-bot

# Оновлення сервісу (Swarm)
docker service update telegram-bot
```

## 🧹 Очищення

```bash
# Видалення контейнера
docker rm -f telegram-bot

# Видалення образу
docker rmi telegram-bot

# Очищення системи
docker system prune -f
```

## 🎭 Налаштування Joke API

### Швидке налаштування

```bash
# В config.env або як змінна середовища
JOKES_API_URL=https://your-api-domain.com/api/jokes/random
JOKES_API_KEY=your_api_key_here  # опціонально
```

### Тестування API

```bash
# Тестовий скрипт
python test_joke.py

# Перевірка API вручну
curl https://your-api-domain.com/api/jokes/random
```

> 📖 **Детальне налаштування**: [API_SETUP.md](API_SETUP.md)

## 🔧 Налаштування середовища

### Локальна розробка

```bash
# .env файл
BOT_TOKEN=your_development_token
BOT_NAME=Dev Bot
LOG_LEVEL=DEBUG
JOKES_API_URL=https://your-api.com/jokes/random
```

### Продакшн

```bash
# Docker з змінними середовища
docker run -d \
  --name telegram-bot \
  -e BOT_TOKEN="YOUR_BOT_TOKEN" \
  -e BOT_NAME="Production Bot" \
  -e JOKES_API_URL="https://your-api.com/jokes/random" \
  telegram-bot
```

## ❓ Часті проблеми

### Помилка "BOT_TOKEN is required"

```bash
# Перевірка токена
echo $BOT_TOKEN

# Для Docker
docker exec telegram-bot printenv BOT_TOKEN
```

### Контейнер не запускається

```bash
# Логи
docker logs telegram-bot

# Статус
docker ps -a
```

### API недоступний

```bash
# Перевірка API
curl https://your-api-domain.com/api/jokes/random

# Логи API
docker logs telegram-bot | grep -i joke
```

## 📞 Допомога

- **Документація**: [README.md](README.md)
- **API налаштування**: [API_SETUP.md](API_SETUP.md)
- **Joke функціонал**: [JOKE_FEATURE.md](JOKE_FEATURE.md)
- **Docker приклади**: [docker-examples.md](docker-examples.md)

---

**Готово! Ваш бот запущений і готовий до роботи! 🎉**