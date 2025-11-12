# Модуль Notify API

## Описание

Модуль для взаимодействия с API сервиса уведомлений о продаже новых автомобилей.

## Структура

### `notify_api_client.py`
Базовый клиент для работы с API уведомлений. Содержит методы для выполнения HTTP-запросов.

### `notify_api_poller.py`
Поллер для получения уведомлений. Наследуется от `NotifyApiClient` и реализует метод `get_new_notifies(bot)` для получения и обработки новых уведомлений.

### `notify_scheduler.py`
Планировщик задач на основе APScheduler для периодического опроса API.

**Основные возможности:**
- Автоматический опрос API с заданным интервалом (по умолчанию каждую секунду)
- Парсинг ответов через Pydantic модели
- Логирование всех операций
- Корректное управление жизненным циклом (start/stop)

**Класс `NotifyScheduler`:**
```python
from app.modules.notify_api.notify_scheduler import get_notify_scheduler

# Создание экземпляра планировщика
scheduler = get_notify_scheduler(bot, interval_seconds=1)

# Запуск планировщика
scheduler.start()

# Остановка планировщика
scheduler.stop()
```

### `notify_api_poller_test.py`
Тестовый класс для ручного тестирования методов API.

## Использование

### Интеграция в приложение

Планировщик автоматически запускается при старте бота в `main.py`:

```python
from app.modules.notify_api.notify_scheduler import get_notify_scheduler

class NewCarSellNotifyBot:
    def __init__(self):
        self.bot = Bot(token=env_config.bot_token.get_secret_value())
        self.dp = Dispatcher()
        # Инициализация планировщика с интервалом 1 секунда
        self.scheduler = get_notify_scheduler(self.bot, interval_seconds=1)
    
    async def start_up_polling(self):
        # Запуск планировщика
        self.scheduler.start()
        
        await self.bot.delete_webhook(drop_pending_updates=True)
        await self.dp.start_polling(self.bot)
```

### Настройка интервала опроса

Вы можете изменить интервал опроса API при создании планировщика:

```python
# Опрос каждые 5 секунд
self.scheduler = get_notify_scheduler(self.bot, interval_seconds=5)

# Опрос каждые 30 секунд
self.scheduler = get_notify_scheduler(self.bot, interval_seconds=30)
```

## Зависимости

- `apscheduler` - для планирования задач
- `aiogram` - для работы с Telegram Bot API
- `aiohttp` - для HTTP-запросов
- `pydantic` - для валидации данных

## Установка зависимостей

```bash
uv pip install apscheduler
```

или через requirements.txt:

```bash
uv pip install -r requirements.txt
```

## Логирование

Все операции логируются с использованием стандартного модуля `logging`:

- `INFO` - успешные операции и количество полученных уведомлений
- `WARNING` - ошибки HTTP-запросов (неверный статус ответа)
- `ERROR` - критические ошибки при работе с API
- `DEBUG` - отсутствие новых уведомлений

## TODO

- [ ] Добавить логику определения получателей уведомлений (chat_id)
- [ ] Реализовать отправку уведомлений конкретным пользователям через бота
- [ ] Добавить фильтрацию уведомлений по критериям
- [ ] Реализовать сохранение истории отправленных уведомлений
