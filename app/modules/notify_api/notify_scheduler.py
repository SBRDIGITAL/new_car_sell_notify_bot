from logging import getLogger
from typing import Optional

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from .notify_api_poller import notify_api_poller
from ...schemas.notify import NewCarNotifyListResponse


logger = getLogger(__name__)



class NotifyScheduler:
    """
    ## Планировщик для получения уведомлений о продаже автомобилей.
    
    Класс управляет периодическим опросом API сервиса уведомлений
    с использованием APScheduler для получения новых уведомлений.
    """
    
    def __init__(self, bot: Bot, interval_seconds: int = 1):
        """
        ## Инициализация планировщика уведомлений.
        
        :param bot: Экземпляр Telegram бота для отправки уведомлений.
        :param interval_seconds: Интервал опроса API в секундах (по умолчанию 1).
        """
        self.bot = bot
        self.interval_seconds = interval_seconds
        self.scheduler: Optional[AsyncIOScheduler] = None
        self._running = False
        
    async def _fetch_and_process_notifies(self):
        """
        ## Получает новые уведомления и обрабатывает их.
        
        Метод вызывается планировщиком с заданным интервалом.
        Получает новые уведомления из API и обрабатывает их.
        
        :raises Exception: При ошибках работы с API или отправки сообщений.
        """
        try:
            async with notify_api_poller:
                data, status, headers = await notify_api_poller._get_new_notifies()
                
                if status == 200 and data:
                    # Парсим ответ с помощью Pydantic модели
                    notify_list = NewCarNotifyListResponse.model_validate(data)
                    
                    if notify_list.data:
                        logger.info(f"Получено {len(notify_list.data)} новых уведомлений")
                        
                        for notify in notify_list.data:
                            # Здесь можно добавить логику отправки уведомлений пользователям
                            logger.info(
                                f"Новое уведомление: "
                                f"URL={notify.advert_url}, "
                                f"Телефон={notify.seller_phone}"
                            )
                            # TODO: Добавить отправку уведомлений через bot
                    else:
                        logger.debug("Новых уведомлений не найдено")
                else:
                    logger.warning(f"Ошибка получения уведомлений: статус {status}")
                    
        except Exception as e:
            logger.error(f"Ошибка при получении уведомлений: {e}", exc_info=True)
    
    def start(self):
        """
        ## Запускает планировщик задач.
        
        Инициализирует и запускает AsyncIOScheduler с заданным интервалом опроса.
        
        :raises RuntimeError: Если планировщик уже запущен.
        """
        if self._running:
            logger.warning("Планировщик уже запущен")
            return
            
        self.scheduler = AsyncIOScheduler()
        self.scheduler.add_job(
            self._fetch_and_process_notifies,
            trigger=IntervalTrigger(seconds=self.interval_seconds),
            id='fetch_notifies',
            name='Получение новых уведомлений',
            replace_existing=True
        )
        
        self.scheduler.start()
        self._running = True
        logger.info(f"Планировщик запущен с интервалом {self.interval_seconds} сек.")
    
    def stop(self):
        """
        ## Останавливает планировщик задач.
        
        Корректно завершает работу планировщика и очищает все задачи.
        """
        if self.scheduler and self._running:
            self.scheduler.shutdown(wait=True)
            self._running = False
            logger.info("Планировщик остановлен")
    
    def is_running(self) -> bool:
        """
        ## Проверяет, запущен ли планировщик.
        
        :return: True если планировщик активен, иначе False.
        :rtype: bool
        """
        return self._running


notify_scheduler: Optional[NotifyScheduler] = None


def get_notify_scheduler(bot: Bot, interval_seconds: int = 1) -> NotifyScheduler:
    """
    ## Возвращает singleton экземпляр планировщика уведомлений.
    
    :param bot: Экземпляр Telegram бота.
    :param interval_seconds: Интервал опроса API в секундах.
    :return: Экземпляр NotifyScheduler.
    :rtype: NotifyScheduler
    """
    global notify_scheduler
    if notify_scheduler is None:
        notify_scheduler = NotifyScheduler(bot, interval_seconds)
    return notify_scheduler
