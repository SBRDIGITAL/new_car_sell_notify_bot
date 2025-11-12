"""
Комбинированный тест: добавление и сразу получение уведомлений.
"""
import asyncio
from logging import basicConfig, INFO

from aiogram import Bot
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties

from app.config.config_reader import env_config
from app.modules.notify.notify_api_client import NotifyApiClient
from app.modules.notify.notify_api_poller import notify_api_poller


basicConfig(
    level=INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


async def combined_test():
    """Добавляет уведомления и сразу их получает."""
    
    print("=" * 70)
    print("🧪 КОМБИНИРОВАННЫЙ ТЕСТ")
    print("=" * 70)
    
    # Тестовые данные
    test_notifications = [
        {
            "advert_url": "https://auto.ru/cars/test/sale/car_001",
            "analytics": "Тестовая машина 1\nОтличное состояние",
            "seller_phone": "+79991111111"
        },
        {
            "advert_url": "https://auto.ru/cars/test/sale/car_002",
            "analytics": "Тестовая машина 2\nСрочная продажа",
            "seller_phone": "+79992222222"
        },
        {
            "advert_url": "https://auto.ru/cars/test/sale/car_003",
            "analytics": "Тестовая машина 3\nИдеальная комплектация",
            "seller_phone": "+79993333333"
        }
    ]
    
    # Шаг 1: Добавляем уведомления
    print("\n📝 ШАГ 1: Добавление уведомлений в API...")
    async with NotifyApiClient() as client:
        for idx, notify_data in enumerate(test_notifications, 1):
            data, status, _ = await client._create_notify(json=notify_data)
            print(f"   [{idx}] Статус: {status}, Ответ: {data}")
    
    print("✅ Уведомления добавлены\n")
    
    # Небольшая задержка для гарантии записи в Redis
    await asyncio.sleep(0.5)
    
    # Шаг 2: Создаем бота
    print("🤖 ШАГ 2: Создание бота...")
    bot = Bot(
        token=env_config.bot_token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    print(f"✅ Бот создан. Администраторы: {env_config.get_admins_tg_ids}\n")
    
    # Шаг 3: Получаем уведомления через поллер
    print("🔄 ШАГ 3: Получение уведомлений через поллер...")
    try:
        async with notify_api_poller:
            data, status, _ = await notify_api_poller.get_new_notifies(bot)
            
            print()
            print("=" * 70)
            print(f"📊 HTTP статус: {status}")
            if data:
                notify_count = len(data.get('data', []))
                print(f"📬 Получено уведомлений: {notify_count}")
                if notify_count > 0:
                    print("\n✅ УСПЕШНО! Уведомления должны быть отправлены администраторам!")
                    print("📱 Проверьте Telegram для подтверждения получения сообщений")
                else:
                    print("\n⚠️  Список уведомлений пуст")
            print("=" * 70)
    
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        await bot.session.close()
        print("\n🛑 Сессия бота закрыта")
        print("\n✅ Тест завершен!")


if __name__ == "__main__":
    asyncio.run(combined_test())
