"""
Тестовый скрипт для проверки работы поллера и отправки уведомлений администраторам.

Этот скрипт запускает поллер один раз для получения уведомлений из API.
"""
import asyncio
from logging import basicConfig, INFO

from aiogram import Bot
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties

from app.config.config_reader import env_config
from app.modules.notify.notify_api_poller import notify_api_poller


# Настраиваем логирование
basicConfig(
    level=INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


async def test_poller():
    """
    Тестирует работу поллера для получения уведомлений.
    
    Создает экземпляр бота, запускает поллер один раз и проверяет,
    что уведомления получены и отправлены администраторам.
    """
    print("=" * 70)
    print("🧪 ТЕСТ: Проверка работы поллера и отправки уведомлений админам")
    print("=" * 70)
    print()
    
    # Создаем бота
    bot = Bot(
        token=env_config.bot_token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    try:
        print("🤖 Бот создан успешно")
        print(f"👥 Администраторы: {env_config.get_admins_tg_ids}")
        print()
        
        # Запускаем поллер
        print("🔄 Запускаем поллер для получения уведомлений...\n")
        
        async with notify_api_poller:
            data, status, headers = await notify_api_poller.get_new_notifies(bot)
            
            print()
            print("=" * 70)
            print("📊 Результат запроса к API:")
            print(f"   HTTP статус: {status}")
            print(f"   Данные: {data}")
            print("=" * 70)
            
            if status == 200:
                if data and data.get('data'):
                    print(f"\n✅ Успешно! Обработано {len(data['data'])} уведомлений")
                    print("💬 Уведомления должны быть отправлены администраторам!")
                else:
                    print("\n⚠️  Новых уведомлений не найдено")
                    print("💡 Запустите сначала test_add_notifies.py для добавления тестовых данных")
            else:
                print(f"\n❌ Ошибка: статус {status}")
    
    except Exception as e:
        print(f"\n❌ Ошибка при выполнении теста: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Закрываем сессию бота
        await bot.session.close()
        print("\n🛑 Сессия бота закрыта")
        print("\n✅ Тест завершен!")


if __name__ == "__main__":
    asyncio.run(test_poller())
