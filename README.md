Мультифункциональный Telegram бот с искусственным интеллектом и векторной базой знаний.

## Описание

Бот позволяет:
- Загружать документы (PDF, DOCX, TXT) для анализа
- Задавать вопросы по содержимому документов (RAG-архитектура)
- Общаться с AI-ассистентом на основе Google Gemini
- Настраивать профиль пользователя
- Просматривать статистику использования

## Быстрый старт

### Вариант 1: Docker (рекомендуется)

1. Клонируйте репозиторий
git clone https://github.com/ТВОЙ_НИК/telegram-ai-assistant.git
cd telegram-ai-assistant

2. Настройте переменные окружения
cp .env.example .env
Отредактируйте .env, добавив BOT_TOKEN и GEMINI_API_KEY

3. Запустите все сервисы одной командой
docker-compose up -d

4. Проверьте логи
docker-compose logs -f bot


### Вариант 2: Локальный запуск

1. Создайте виртуальное окружение
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

2. Установите зависимости
pip install -r requirements.txt

3. Запустите базу данных (Docker)
docker-compose up

4. Запустите бота
python src/bot/main.py

## Получение токенов
### Telegram Bot Token:
1. Откройте @BotFather
2. Отправьте /newbot
3. Следуйте инструкциям
### Google Gemini API Key:
1. Перейдите на Google AI Studio
2. Войдите через Google аккаунт
3. Нажмите "Create API key"