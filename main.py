import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties

from app.config.config_reader import env_config



class NewCarSellNotifyBot:
    """Бот для уведомлений о продаже новых автомобилей.
    
    Класс представляет собой Telegram-бота, который использует библиотеку aiogram
    для работы с Telegram Bot API. Бот предназначен для отправки уведомлений
    о продаже новых автомобилей.
    
    Attributes:
        bot (Bot): Экземпляр бота aiogram с настроенными параметрами.
        dp (Dispatcher): Диспетчер для обработки входящих сообщений и команд.
    """

    def __init__(self):
        """Инициализирует экземпляр бота для уведомлений о продаже автомобилей.
        
        Создает экземпляр Bot с токеном из конфигурации и настройками по умолчанию,
        а также инициализирует Dispatcher для обработки сообщений.
        
        Raises:
            ValueError: Если токен бота не найден в конфигурации.
            ConnectionError: Если не удается установить соединение с Telegram API.
        """
        self.bot = Bot(
            token=env_config.bot_token.get_secret_value(),
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        self.dp = Dispatcher()

    async def start_up_polling(self):
        """Запускает polling бота в асинхронном режиме.
        
        Метод удаляет webhook (если он был установлен) и запускает длительное 
        соединение (long polling) для получения обновлений от Telegram.
        Обеспечивает корректное завершение работы при получении сигнала прерывания.
        
        Raises:
            TelegramAPIError: При ошибках взаимодействия с Telegram API.
            ConnectionError: При проблемах с сетевым соединением.
            
        Note:
            Метод блокирующий и будет выполняться до получения сигнала остановки.
        """        
        try:
            await self.bot.delete_webhook(drop_pending_updates=True)
            await self.dp.start_polling(self.bot)
        except KeyboardInterrupt:
            print("Получен сигнал остановки...")
        finally:
            await self.bot.session.close()
            print("Бот остановлен.")

    async def run(self):
        """Основной метод для запуска бота.
        
        Запускает бота в режиме polling и обеспечивает его работу до получения
        сигнала остановки. Является точкой входа для запуска всех функций бота.
        
        Raises:
            Exception: Любые исключения, возникшие при работе бота, будут
                      переданы вызывающему коду для обработки.
        """
        await self.start_up_polling()


async def main():
    """Точка входа в приложение.
    
    Создает экземпляр бота для уведомлений о продаже автомобилей и запускает его.
    Функция служит основной асинхронной точкой входа для всего приложения.
    
    Raises:
        Exception: Любые исключения, возникшие при инициализации или работе бота.
    """
    bot_instance = NewCarSellNotifyBot()
    await bot_instance.run()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Приложение остановлено пользователем.")