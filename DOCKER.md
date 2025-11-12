# Docker для New Car Sell Notify Bot

Инструкции по запуску бота в Docker контейнере.

## Предварительные требования

- ✅ Docker установлен и запущен
- ✅ Docker Compose установлен (обычно идёт с Docker Desktop)
- ✅ Файл `.env` настроен с правильными параметрами
- ✅ API сервис уведомлений доступен (если запущен на хосте)

## Конфигурация для Docker

### 1. Подключение к API на хосте

Если API запущен локально на хосте (вне Docker), в `.env` используйте:

```env
NOTIFY_API_HOST='host.docker.internal'
NOTIFY_API_PORT=8000
```

`host.docker.internal` - специальный DNS имя Docker, которое указывает на хост-машину.

### 2. Подключение к API в Docker сети

Если API тоже в docker-compose, используйте имя сервиса:

```env
NOTIFY_API_HOST='notify_api_service'
NOTIFY_API_PORT=8000
```

## Структура файлов

```
.
├── Dockerfile              # Образ бота
├── docker-compose.yml      # Оркестрация контейнера
├── .dockerignore          # Исключения при сборке образа
├── .env                   # Переменные окружения (не коммитить!)
├── requirements.txt       # Зависимости Python
└── main.py               # Точка входа приложения
```

## Команды Docker

### Сборка образа

```bash
docker compose build
```

Или с очисткой кэша:

```bash
docker compose build --no-cache
```

### Запуск бота

```bash
docker compose up
```

В фоновом режиме (detached):

```bash
docker compose up -d
```

### Остановка бота

```bash
docker compose down
```

### Просмотр логов

Все логи:
```bash
docker compose logs
```

Логи в реальном времени:
```bash
docker compose logs -f
```

Последние N строк:
```bash
docker compose logs --tail=100
```

Логи конкретного сервиса:
```bash
docker compose logs new_car_sell_notify_bot
```

### Перезапуск бота

```bash
docker compose restart
```

### Полная пересборка и перезапуск

```bash
docker compose down
docker compose build --no-cache
docker compose up -d
```

## Управление контейнером

### Проверка статуса

```bash
docker compose ps
```

### Вход в контейнер (debugging)

```bash
docker compose exec new_car_sell_notify_bot bash
```

Или через `sh` (если bash недоступен):
```bash
docker compose exec new_car_sell_notify_bot sh
```

### Проверка переменных окружения в контейнере

```bash
docker compose exec new_car_sell_notify_bot env
```

## Переменные окружения

Основные переменные в `.env`:

```env
# Bot
BOT_TOKEN='YOUR_BOT_TOKEN_HERE'
ADMINS_TG_IDS='123456789,987654321'

# Notify API
NOTIFY_API_HOST='host.docker.internal'  # для локального API
NOTIFY_API_PORT=8000

# Environment
ENV='production'
```

## Troubleshooting

### Проблема: Бот не может подключиться к API

**Решение 1:** Проверьте `NOTIFY_API_HOST`
- Для API на хосте: `host.docker.internal`
- Для API в Docker: имя сервиса из docker-compose

**Решение 2:** Убедитесь, что API запущен и доступен:
```bash
curl http://localhost:8000/v1/lifecheck
```

### Проблема: "Cannot connect to Docker daemon"

**Решение:** Убедитесь, что Docker Desktop запущен:
```bash
docker ps
```

### Проблема: Изменения кода не применяются

**Решение:** Пересоберите образ:
```bash
docker compose down
docker compose build --no-cache
docker compose up -d
```

### Проблема: Нет логов в консоли

**Решение:** Логи настроены на stdout. Смотрите через:
```bash
docker compose logs -f
```

### Проблема: Контейнер постоянно перезапускается

**Решение:** Проверьте логи на ошибки:
```bash
docker compose logs --tail=50
```

Проверьте конфигурацию `.env` и доступность API.

## Production рекомендации

1. **Используйте Docker secrets** вместо `.env` файла для токенов:
   ```yaml
   secrets:
     - bot_token
   ```

2. **Настройте health checks**:
   ```yaml
   healthcheck:
     test: ["CMD", "python", "-c", "import sys; sys.exit(0)"]
     interval: 30s
     timeout: 10s
     retries: 3
   ```

3. **Ограничьте ресурсы**:
   ```yaml
   deploy:
     resources:
       limits:
         cpus: '0.5'
         memory: 512M
       reservations:
         memory: 256M
   ```

4. **Используйте multi-stage builds** для оптимизации размера образа

5. **Настройте логирование** через Docker logging driver:
   ```yaml
   logging:
     driver: "json-file"
     options:
       max-size: "10m"
       max-file: "3"
   ```

## Docker сеть

Бот использует выделенную сеть `new_car_sell_notify_net` типа bridge для изоляции и возможности связи с другими сервисами.

## Volumes

Бот не использует volumes, так как не хранит данные локально. Все данные находятся в API сервисе.

## Быстрый старт

```bash
# 1. Убедитесь, что .env настроен
cat .env

# 2. Соберите образ
docker compose build

# 3. Запустите бот
docker compose up -d

# 4. Проверьте логи
docker compose logs -f

# 5. Для остановки
docker compose down
```

## Полезные команды

```bash
# Проверить использование ресурсов
docker stats new_car_sell_notify_bot

# Удалить неиспользуемые образы
docker image prune

# Удалить всё неиспользуемое (осторожно!)
docker system prune -a

# Экспортировать образ
docker save new_car_sell_notify_bot:latest | gzip > bot_image.tar.gz

# Импортировать образ
docker load < bot_image.tar.gz
```

## Обновление

```bash
# 1. Остановить бота
docker compose down

# 2. Получить новый код (git pull или обновить файлы)
git pull

# 3. Пересобрать образ
docker compose build

# 4. Запустить обновлённую версию
docker compose up -d

# 5. Проверить логи
docker compose logs -f --tail=50
```
