# 📊 Statistics Feature

> **Навігація**: [README.md](README.md) ← [QUICK_START.md](QUICK_START.md)

## Огляд

Система статистики дозволяє відстежувати активність користувачів, аналізувати використання бота та надавати адміністраторам детальну інформацію про роботу бота.

## Функціональність

### 📈 Статистика бота
- **Час роботи** - скільки часу бот працює без перезапуску
- **Останній запуск** - коли бот був останній раз перезапущений
- **Кількість користувачів** - загальна кількість унікальних користувачів
- **Активні користувачі** - кількість користувачів за останні 24 години
- **Повідомлення** - загальна кількість повідомлень та команд
- **Топ команд** - найпопулярніші команди

### 👥 Відстеження користувачів
- **Унікальні ID** - зберігання ID всіх користувачів
- **Профіль користувача** - username, ім'я, прізвище
- **Активність** - коли користувач вперше та останній раз писав
- **Статистика використання** - кількість повідомлень та команд
- **Історія команд** - які команди використовував користувач

### 🔐 Адміністративний панель
- **Список користувачів** - всі користувачі з детальною інформацією
- **Авторизація** - доступ тільки для адміністраторів
- **Реальний час** - оновлення даних в реальному часі
- **Експорт даних** - збереження в JSON форматі

## Команди

### `/stats`
Показує детальну статистику бота:
```
📊 Статистика бота

🕐 Останній запуск: 27.09.2025 20:30:15 UTC
⏱️ Час роботи: 2г 15хв

👥 Користувачі:
• Всього: 25
• За останні 24 год: 8

📨 Повідомлення:
• Всього: 156
• Команд: 89

🔥 Топ команд:
• /start: 25
• /joke: 18
• /menu: 15
• /help: 12
• /info: 8
```

### `/admin`
Адміністративна панель (тільки для адміністраторів):
```
👥 Список користувачів:

1. **John Doe** (@johndoe)
   ID: `123456789` | Останній візит: 27.09 20:25
   Повідомлень: 15

2. **Jane Smith** (@janesmith)
   ID: `987654321` | Останній візит: 27.09 19:45
   Повідомлень: 8

3. **User** (@unknown)
   ID: `555666777` | Останній візит: 27.09 18:30
   Повідомлень: 3

... та ще 22 користувачів
```

## Конфігурація

### Змінні середовища

| Змінна | Опис | Приклад |
|--------|------|---------|
| `ADMIN_USER_IDS` | ID адміністраторів (через кому) | `123456789,987654321` |
| `STATS_DATA_DIR` | Папка для збереження даних | `data` |

### Приклад конфігурації

```bash
# .env файл
ADMIN_USER_IDS=123456789,987654321
STATS_DATA_DIR=data
```

## Архітектура

### Структура даних

#### UserStats
```python
@dataclass
class UserStats:
    user_id: int
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    first_seen: str
    last_seen: str
    message_count: int
    commands_used: Dict[str, int]
```

#### BotStats
```python
@dataclass
class BotStats:
    start_time: str
    last_restart: str
    total_users: int
    total_messages: int
    total_commands: int
    commands_breakdown: Dict[str, int]
```

### Зберігання даних

#### JSON файли
- **`data/users.json`** - дані користувачів
- **`data/bot_stats.json`** - статистика бота

#### Формат збереження
```json
{
  "123456789": {
    "user_id": 123456789,
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe",
    "first_seen": "2025-09-27T18:15:30+00:00",
    "last_seen": "2025-09-27T20:25:45+00:00",
    "message_count": 15,
    "commands_used": {
      "/start": 1,
      "/joke": 5,
      "/menu": 3
    }
  }
}
```

## Безпека

### Авторизація адміністраторів
- Перевірка User ID при використанні `/admin`
- Список адміністраторів в конфігурації
- Відмова в доступі для неавторизованих користувачів

### Захист даних
- Локальне зберігання даних
- Шифрування не вимагається (публічні дані)
- Автоматичне резервне копіювання

## Використання

### Локальний запуск
```bash
# 1. Налаштування
export ADMIN_USER_IDS="123456789,987654321"
export STATS_DATA_DIR="data"

# 2. Запуск
python main.py
```

### Docker
```bash
# Запуск з адміністраторами
docker run -d \
  --name telegram-bot \
  -e BOT_TOKEN="YOUR_BOT_TOKEN" \
  -e ADMIN_USER_IDS="123456789,987654321" \
  -e STATS_DATA_DIR="data" \
  -v $(pwd)/data:/app/data \
  telegram-bot
```

### Docker Compose
```yaml
services:
  telegram-bot:
    build: .
    environment:
      - BOT_TOKEN=${BOT_TOKEN}
      - ADMIN_USER_IDS=123456789,987654321
      - STATS_DATA_DIR=data
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```

## Діагностика

### Перевірка статистики
```bash
# Перевірка файлів даних
ls -la data/
cat data/users.json | jq
cat data/bot_stats.json | jq

# Логи
docker logs telegram-bot | grep "User interaction tracked"
docker logs telegram-bot | grep "Command usage tracked"
```

### Тестування
```python
# Тест статистики
from stats import stats_manager

# Отримати статистику
stats = stats_manager.get_bot_stats()
print(f"Total users: {stats.total_users}")

# Отримати користувачів
users = stats_manager.get_all_users()
for user in users[:5]:
    print(f"User: {user.first_name} (@{user.username})")
```

## Розширення

### Додавання нових метрик
```python
# В stats.py
def track_custom_metric(self, user_id: int, metric: str, value: int):
    """Track custom metric for user"""
    if user_id in self.users:
        if metric not in self.users[user_id].custom_metrics:
            self.users[user_id].custom_metrics[metric] = 0
        self.users[user_id].custom_metrics[metric] += value
```

### Експорт даних
```python
# Експорт в CSV
import csv

def export_users_csv(self, filename: str):
    """Export users to CSV file"""
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['User ID', 'Username', 'First Name', 'Last Name', 'Messages', 'Last Seen'])
        for user in self.users.values():
            writer.writerow([
                user.user_id, user.username, user.first_name, 
                user.last_name, user.message_count, user.last_seen
            ])
```

## Troubleshooting

### Проблема: Статистика не зберігається
```bash
# Перевірка прав доступу
ls -la data/
chmod 755 data/
chown -R 1000:1000 data/
```

### Проблема: Адміністратор не може використовувати /admin
```bash
# Перевірка конфігурації
echo $ADMIN_USER_IDS
docker exec telegram-bot printenv ADMIN_USER_IDS
```

### Проблема: Дані втрачаються при перезапуску
```bash
# Перевірка монтування томів
docker inspect telegram-bot | grep Mounts
```

## Навігація

- [README.md](README.md) - Головна документація
- [QUICK_START.md](QUICK_START.md) - Швидкий старт
- [JOKE_FEATURE.md](JOKE_FEATURE.md) - Функція жартів
- [API_SETUP.md](API_SETUP.md) - Налаштування API
