"""
Тестовый скрипт для добавления 3 уведомлений в API.

Этот скрипт добавляет тестовые уведомления о продаже автомобилей
для проверки работы поллера и отправки уведомлений администраторам.
"""
import asyncio
from app.modules.notify.notify_api_client import NotifyApiClient


async def add_test_notifies():
    """
    Добавляет 3 тестовых уведомления в API.
    
    Каждое уведомление содержит:
    - URL объявления
    - Аналитическую информацию об автомобиле
    - Телефон продавца в международном формате
    """
    # Тестовые данные для уведомлений
    test_notifications = [
        {
            "advert_url": "https://auto.ru/cars/used/sale/toyota_camry_2020_123456",
            "analytics": (
                "🚗 Toyota Camry 2020\n"
                "💰 Цена: 2 500 000 руб.\n"
                "📍 Москва\n"
                "🔧 Состояние: отличное\n"
                "👤 Один владелец\n"
                "📊 Пробег: 45 000 км\n"
                "✅ Полная история обслуживания"
            ),
            "seller_phone": "+79991234567"
        },
        {
            "advert_url": "https://auto.ru/cars/used/sale/bmw_x5_2019_987654",
            "analytics": (
                "🚙 BMW X5 2019\n"
                "💰 Цена: 4 200 000 руб.\n"
                "📍 Санкт-Петербург\n"
                "🔧 Состояние: идеальное\n"
                "👤 Срочная продажа\n"
                "📊 Пробег: 28 000 км\n"
                "✅ Полная комплектация M-Sport"
            ),
            "seller_phone": "+79997654321"
        },
        {
            "advert_url": "https://auto.ru/cars/used/sale/mercedes_e_class_2021_555888",
            "analytics": (
                "🚘 Mercedes-Benz E-Class 2021\n"
                "💰 Цена: 5 800 000 руб.\n"
                "📍 Екатеринбург\n"
                "🔧 Состояние: как новый\n"
                "👤 Официальный дилер\n"
                "📊 Пробег: 12 000 км\n"
                "✅ Гарантия до 2026 года"
            ),
            "seller_phone": "+79993331122"
        }
    ]
    
    # Создаем клиент API
    async with NotifyApiClient() as client:
        print("🚀 Начинаем добавление тестовых уведомлений...\n")
        
        success_count = 0
        error_count = 0
        
        # Добавляем каждое уведомление
        for idx, notify_data in enumerate(test_notifications, 1):
            try:
                print(f"[{idx}/3] Добавление уведомления: {notify_data['advert_url']}")
                
                data, status, headers = await client._create_notify(json=notify_data)
                
                if status == 200:
                    success_count += 1
                    print(f"✅ Успешно добавлено (статус: {status})")
                    if data:
                        print(f"   Ответ: {data}")
                else:
                    error_count += 1
                    print(f"❌ Ошибка (статус: {status})")
                    print(f"   Данные: {data}")
                
                print()  # Пустая строка для читаемости
                
            except Exception as e:
                error_count += 1
                print(f"❌ Исключение при добавлении: {e}\n")
        
        # Итоговая статистика
        print("=" * 60)
        print("📊 Результаты:")
        print(f"   ✅ Успешно добавлено: {success_count}")
        print(f"   ❌ Ошибок: {error_count}")
        print(f"   📝 Всего попыток: {len(test_notifications)}")
        print("=" * 60)
        
        if success_count > 0:
            print("\n💡 Теперь поллер должен подтянуть эти уведомления")
            print("   и отправить их администраторам через Telegram!")


if __name__ == "__main__":
    print("=" * 60)
    print("🧪 ТЕСТ: Добавление уведомлений в API")
    print("=" * 60)
    print()
    
    asyncio.run(add_test_notifies())
    
    print("\n✅ Тест завершен!")
