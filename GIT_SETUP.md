# 🚀 Налаштування Git репозиторію

## Підготовка до першого commit

### 1. Ініціалізація репозиторію

```bash
# Ініціалізація git репозиторію
git init

# Додавання remote origin (замініть на ваш URL)
git remote add origin https://github.com/yourusername/telegram-bot.git

# Перевірка remote
git remote -v
```

### 2. Перший commit

```bash
# Додавання всіх файлів
git add .

# Перевірка статусу
git status

# Перший commit
git commit -m "🎉 Initial commit: Telegram Bot with Docker support

- Add modular bot architecture with handlers
- Add Docker support with secrets and environment variables
- Add Joke API integration with external API support
- Add comprehensive documentation with navigation
- Add security features with Docker secrets
- Add testing scripts and examples
- Add contributing guidelines and changelog"

# Push в репозиторій
git push -u origin main
```

## Структура проекту

```
telegram-bot/
├── 📁 handlers/              # Обробники подій
│   ├── __init__.py
│   ├── command_handlers.py   # Команди (/start, /help, /joke)
│   ├── message_handlers.py   # Повідомлення користувачів
│   ├── callback_handlers.py # Інтерактивні кнопки
│   └── error_handlers.py     # Обробка помилок
├── 📄 main.py               # Точка входу
├── 📄 config.py             # Конфігурація
├── 📄 utils.py              # Допоміжні функції
├── 🐳 Dockerfile            # Docker образ
├── 🐳 docker-compose.yml    # Docker Compose
├── 📄 requirements.txt      # Залежності
├── 📄 config.env            # Приклад конфігурації
├── 🧪 test_joke.py          # Тестовий скрипт
├── 📚 README.md             # Головна документація
├── 📚 QUICK_START.md        # Швидкий старт
├── 📚 API_SETUP.md          # Налаштування API
├── 📚 JOKE_FEATURE.md       # Joke функціонал
├── 📚 docker-examples.md    # Docker приклади
├── 📚 CONTRIBUTING.md       # Інструкції для внеску
├── 📚 CHANGELOG.md          # Історія змін
├── 📄 LICENSE               # MIT ліцензія
├── 📄 .gitignore            # Git ignore правила
└── 📄 .gitattributes        # Git атрибути
```

## Налаштування GitHub репозиторію

### 1. Створення репозиторію на GitHub

1. Перейдіть на [GitHub](https://github.com)
2. Натисніть "New repository"
3. Заповніть деталі:
   - **Repository name**: `telegram-bot`
   - **Description**: `Modular Telegram Bot with Docker support and external API integration`
   - **Visibility**: Public або Private
   - **Initialize**: НЕ створюйте README, .gitignore, LICENSE (вони вже є)

### 2. Налаштування репозиторію

```bash
# Клонування (якщо створюєте новий репозиторій)
git clone https://github.com/yourusername/telegram-bot.git
cd telegram-bot

# Або додавання remote до існуючого проекту
git remote add origin https://github.com/yourusername/telegram-bot.git
```

### 3. Налаштування GitHub Actions (опціонально)

Створіть файл `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest black flake8 mypy
    
    - name: Lint with flake8
      run: |
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
    
    - name: Check formatting with black
      run: |
        black --check .
    
    - name: Type check with mypy
      run: |
        mypy .
    
    - name: Test with pytest
      run: |
        pytest
```

## Налаштування захисту

### 1. Захист головної гілки

1. Перейдіть в Settings → Branches
2. Додайте rule для `main` гілки:
   - ✅ Require pull request reviews
   - ✅ Require status checks to pass
   - ✅ Require branches to be up to date

### 2. Налаштування секретів

1. Перейдіть в Settings → Secrets and variables → Actions
2. Додайте необхідні секрети:
   - `BOT_TOKEN` - токен Telegram бота
   - `JOKES_API_URL` - URL вашого API
   - `JOKES_API_KEY` - API ключ (опціонально)

## Теги та релізи

### 1. Створення тегу

```bash
# Створення тегу
git tag -a v1.0.0 -m "Release version 1.0.0"

# Push тегу
git push origin v1.0.0
```

### 2. Створення релізу на GitHub

1. Перейдіть в Releases
2. Натисніть "Create a new release"
3. Заповніть деталі:
   - **Tag**: `v1.0.0`
   - **Title**: `v1.0.0 - Initial Release`
   - **Description**: Скопіюйте з CHANGELOG.md

## Налаштування Issues та Projects

### 1. Налаштування шаблонів

Створіть `.github/ISSUE_TEMPLATE/bug_report.md`:

```markdown
---
name: Bug report
about: Create a report to help us improve
title: ''
labels: bug
assignees: ''
---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment:**
 - OS: [e.g. Ubuntu 20.04]
 - Python version: [e.g. 3.11]
 - Docker version: [e.g. 20.10]
 - Bot version: [e.g. 1.0.0]

**Additional context**
Add any other context about the problem here.
```

### 2. Налаштування Projects

1. Перейдіть в Projects
2. Створіть новий проект "Telegram Bot Development"
3. Налаштуйте колонки:
   - 📋 Backlog
   - 🔄 In Progress
   - 👀 Review
   - ✅ Done

## Моніторинг та аналітика

### 1. GitHub Insights

- **Traffic** - перегляди та клони
- **Contributors** - активні контрибутори
- **Community** - health score

### 2. Налаштування Codecov (опціонально)

```yaml
# .github/workflows/coverage.yml
name: Coverage

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  coverage:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest-cov
    
    - name: Run tests with coverage
      run: |
        pytest --cov=. --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
```

## Команди для роботи з репозиторієм

### Основні команди

```bash
# Перевірка статусу
git status

# Додавання файлів
git add .

# Commit з повідомленням
git commit -m "feat: add new feature"

# Push змін
git push origin main

# Pull останніх змін
git pull origin main

# Перегляд історії
git log --oneline

# Створення гілки
git checkout -b feature/new-feature

# Перемикання гілок
git checkout main
```

### Корисні команди

```bash
# Перегляд змін
git diff

# Скасування змін
git checkout -- filename

# Скасування commit
git reset --soft HEAD~1

# Очищення невідстежуваних файлів
git clean -fd

# Перегляд remote
git remote -v

# Оновлення remote
git remote set-url origin https://github.com/yourusername/telegram-bot.git
```

## Готово! 🎉

Ваш проект готовий до роботи з Git! Всі необхідні файли створені та налаштовані.

### Наступні кроки:

1. **Створіть репозиторій** на GitHub
2. **Налаштуйте remote** origin
3. **Зробіть перший commit**
4. **Налаштуйте захист** гілок
5. **Створіть перший реліз**

---

**Успішного розвитку проекту! 🚀**
