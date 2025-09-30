# 🐳 Docker Examples

> **Навігація**: [README.md](README.md) ← [docker-examples.md](docker-examples.md) → [QUICK_START.md](QUICK_START.md)

## 🚀 Швидкий старт

### 1. Мінімальний запуск

```bash
# Створення секрету
# BOT_TOKEN передається через змінну середовища

# Запуск контейнера
docker run -d \
  --name telegram-bot \
  -e BOT_TOKEN="YOUR_BOT_TOKEN" \
  telegram-bot
```

### 2. Запуск з налаштуваннями

```bash
# Створення секрету
# BOT_TOKEN передається через змінну середовища

# Запуск з змінними середовища
docker run -d \
  --name telegram-bot \
  -e BOT_TOKEN="YOUR_BOT_TOKEN" \
  -e BOT_NAME="My Awesome Bot" \
  -e BOT_DEVELOPER="Your Name" \
  -e LOG_LEVEL=DEBUG \
  telegram-bot
```

### 3. Docker Compose (рекомендовано)

```bash
# Створення .env файлу
cat > .env << EOF
BOT_NAME=My Telegram Bot
BOT_DEVELOPER=Your Name
BOT_EMAIL=your.email@example.com
LOG_LEVEL=INFO
EOF

# Створення секрету
# BOT_TOKEN передається через змінну середовища

# Запуск
docker-compose up -d
```

## 🐳 Docker Swarm

### 1. Ініціалізація кластера

```bash
# На головному вузлі
docker swarm init

# На робочих вузлах
docker swarm join --token SWMTKN-1-xxx manager-ip:2377
```

### 2. Налаштування змінних середовища

```bash
# BOT_TOKEN передається через змінну середовища
# Перевірка змінних
echo $BOT_TOKEN
```

### 3. Запуск сервісу

```bash
# Створення сервісу
docker service create \
  --name telegram-bot \
  -e BOT_TOKEN="YOUR_BOT_TOKEN" \
  --env BOT_NAME="Production Bot" \
  --env LOG_LEVEL=INFO \
  --replicas 1 \
  telegram-bot

# Масштабування
docker service scale telegram-bot=3

# Перегляд статусу
docker service ps telegram-bot
```

## 🔍 Моніторинг та логування

### 2. Централізоване логування

```bash
# З Fluentd
docker run -d \
  --name telegram-bot \
  -e BOT_TOKEN="YOUR_BOT_TOKEN" \
  --log-driver=fluentd \
  --log-opt fluentd-address=localhost:24224 \
  telegram-bot

# З ELK Stack
docker run -d \
  --name telegram-bot \
  -e BOT_TOKEN="YOUR_BOT_TOKEN" \
  --log-driver=json-file \
  --log-opt max-size=10m \
  --log-opt max-file=3 \
  telegram-bot
```

### 3. Health Check

```bash
# Додайте в Dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import sys; sys.exit(0)" || exit 1
```

## 🚀 Автоматизація

### 1. Автоматичне оновлення з Watchtower

```bash
# Запуск Watchtower
docker run -d \
  --name watchtower \
  -v /var/run/docker.sock:/var/run/docker.sock \
  containrrr/watchtower telegram-bot
```

### 2. CI/CD з GitHub Actions

```yaml
# .github/workflows/docker.yml
name: Build and Deploy
on:
  push:
    branches: [main]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Build Docker image
      run: docker build -t telegram-bot .
    - name: Deploy to server
      run: |
        docker service update --image telegram-bot telegram-bot
```

## 🔧 Налагодження

### 3. Тестування

```bash
# Запуск тестів в контейнері
docker run --rm telegram-bot python -m pytest

# Запуск з відладкою
docker run -it --rm telegram-bot python -c "import config; print(config.Config.get_bot_info())"
```

## Посилання

- **Швидкий старт**: [QUICK_START.md](QUICK_START.md)
- **API налаштування**: [API_SETUP.md](API_SETUP.md)
- **Joke функціонал**: [JOKE_FEATURE.md](JOKE_FEATURE.md)
- **Головна документація**: [README.md](README.md)

---

**Docker приклади готові до використання! 🐳**
