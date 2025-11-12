"""
Прямая проверка API без использования клиента.
"""
import asyncio
import aiohttp


async def direct_api_test():
    """Прямой тест API через aiohttp."""
    
    base_url = "http://localhost:8000/v1/"
    
    print("=" * 70)
    print("🧪 ПРЯМОЙ ТЕСТ API")
    print("=" * 70)
    
    async with aiohttp.ClientSession() as session:
        # Шаг 1: Добавляем уведомление
        print("\n📝 ШАГ 1: POST - Добавление уведомления...")
        notify_data = {
            "advert_url": "https://test.com/car/999",
            "analytics": "Прямой тест API",
            "seller_phone": "+79999999999"
        }
        
        async with session.post(f"{base_url}notify/", json=notify_data) as resp:
            status = resp.status
            data = await resp.json()
            print(f"   Статус: {status}")
            print(f"   Ответ: {data}")
        
        # Задержка
        await asyncio.sleep(0.5)
        
        # Шаг 2: Получаем уведомления
        print("\n🔄 ШАГ 2: GET - Получение уведомлений...")
        async with session.get(f"{base_url}notify/") as resp:
            status = resp.status
            data = await resp.json()
            print(f"   Статус: {status}")
            print(f"   Ответ: {data}")
            print(f"   Количество: {len(data.get('data', []))}")
        
        # Шаг 3: Еще раз GET - проверяем, что очистились
        print("\n🔄 ШАГ 3: GET - Повторное получение (должно быть пусто)...")
        async with session.get(f"{base_url}notify/") as resp:
            status = resp.status
            data = await resp.json()
            print(f"   Статус: {status}")
            print(f"   Ответ: {data}")
            print(f"   Количество: {len(data.get('data', []))}")
    
    print("\n✅ Тест завершен!")


if __name__ == "__main__":
    asyncio.run(direct_api_test())
