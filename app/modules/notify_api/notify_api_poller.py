from logging import getLogger

from aiogram import Bot

from .notify_api_client import NotifyApiClient
from ...schemas.notify import NewCarNotifyListResponse


logger = getLogger(__name__)



class NotifyApiPoller(NotifyApiClient):
    """
    ## Поллер сервиса уведомлений.
    
    Класс для взаимодействия с API сервиса уведомлений.
    Предоставляет методы для выполнения HTTP-запросов к API.
    """
    def __init__(self):
        """
        ## Инициализация поллера.
        
        :param api_version: Версия API для использования (по умолчанию 1).
        """
        super().__init__()

    async def get_new_notifies(self, bot: Bot):
        """
        ## Получает новые уведомления о продаже автомобилей.
        
        Выполняет запрос к API для получения списка новых уведомлений,
        обрабатывает их и отправляет через Telegram бота.
        
        :param bot: Экземпляр Telegram бота для отправки уведомлений.
        :return: Кортеж (данные, HTTP статус, заголовки).
        :rtype: tuple[Any, int, dict]
        :raises Exception: При ошибках работы с API.
        """
        try:
            data, status, headers = await self._get_new_notifies()
            
            if status == 200 and data:
                # Парсим ответ с помощью Pydantic модели
                notify_list = NewCarNotifyListResponse.model_validate(data)
                
                if notify_list.data:
                    logger.info(f"Получено {len(notify_list.data)} новых уведомлений")
                    
                    for notify in notify_list.data:
                        # Формируем сообщение для отправки
                        message = (
                            f"🚗 <b>Новое объявление о продаже автомобиля</b>\n\n"
                            f"📊 <b>Аналитика:</b>\n{notify.analytics}\n\n"
                            f"📱 <b>Телефон продавца:</b> {notify.seller_phone}\n"
                            f"🔗 <b>Ссылка:</b> {notify.advert_url}"
                        )
                        
                        # TODO: Добавить логику определения получателей (chat_id)
                        # Пока логируем, позже нужно добавить отправку конкретным пользователям
                        logger.info(f"Новое уведомление: {message}")
                        
                        # Пример отправки (раскомментировать когда будет настроена логика получателей):
                        # await bot.send_message(chat_id=ADMIN_CHAT_ID, text=message)
                else:
                    logger.debug("Новых уведомлений не найдено")
            else:
                logger.warning(f"Ошибка получения уведомлений: статус {status}")
            
            return data, status, headers
            
        except Exception as e:
            logger.error(f"Ошибка при получении уведомлений: {e}", exc_info=True)
            raise
    

notify_api_poller = NotifyApiPoller()