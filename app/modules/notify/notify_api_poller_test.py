from logging import getLogger

from .notify_api_poller import NotifyApiPoller
from ...schemas.notify import NewCarNotify


logger = getLogger(__name__)


class NotifyApiPollerTest(NotifyApiPoller):
    """
    ## Тестовый класс для поллера сервиса уведомлений.
    
    Предоставляет методы для тестирования API сервиса уведомлений.
    Содержит набор тестовых методов для проверки различных эндпоинтов API.
    """

    def __init__(self):
        """
        ## Инициализация тестового поллера.
        
        Вызывает конструктор родительского класса для настройки базового функционала.
        """
        super().__init__()

    @property
    def test_methods(self):
        """
        ## Возвращает список ссылок на тестовые методы.
        
        Предоставляет список методов для последовательного выполнения тестов API.
        
        :return: Список ссылок на методы тестирования.
        :rtype: list[callable]
        """
        return [
            self.run_lifecheck,
            self.run_create_notify,
            self.run_get_new_notifies
        ]

    async def run_lifecheck(self):
        """
        ## Выполняет запрос к эндпоинту проверки состояния сервиса.
        
        Тестирует доступность API через healthcheck эндпоинт.
        
        :return: Кортеж (данные ответа, HTTP статус, заголовки ответа).
        :rtype: tuple[Any, int, dict]
        """
        return await self._run_lifecheck()
    
    async def run_create_notify(self):
        """
        ## Выполняет запрос на создание уведомления о продаже автомобиля.
        
        Создаёт тестовое уведомление с фиксированными данными и отправляет 
        его на сервер через API. Используется для проверки работоспособности
        эндпоинта создания уведомлений.
        
        :return: Кортеж (данные ответа, HTTP статус, заголовки ответа).
        :rtype: tuple[Any, int, dict]
        """
        new_car_notify = NewCarNotify(
            advert_url='https://t.me/car/123',
            analytics='Тестовая анатилитика',
            seller_phone='+79205678901'
        )
        return await self._create_notify(json=new_car_notify.model_dump(mode='json'))

    async def run_get_new_notifies(self):
        """
        ## Выполняет запрос на получение новых уведомлений.
        
        Получает список новых уведомлений о продаже автомобилей с сервера.
        Используется для проверки работоспособности эндпоинта получения уведомлений.
        
        :return: Кортеж (список уведомлений, HTTP статус, заголовки ответа).
        :rtype: tuple[Any, int, dict]
        """
        return await self._get_new_notifies()
    
    async def run_methods(self):
        """
        ## Выполняет все тестовые методы последовательно.
        
        Запускает HTTP-клиент в контекстном менеджере и последовательно 
        выполняет все тестовые методы из списка `test_methods`.
        Для каждого метода выводит результат выполнения запроса.
        
        :raises RuntimeError: Если клиент не был инициализирован.
        :raises aiohttp.ClientError: При ошибках HTTP-запросов.
        
        Note:
            Метод автоматически управляет жизненным циклом HTTP-клиента.
        """
        async with self.client:
            for method in self.test_methods:
                try:
                    result = await method()
                    data, status, header = result
                    logger.info(f"Ответ сервера от {method.__name__}: {result}")
                    logger.debug(f'data={data}, status={status}, header={header}')
                except Exception as e:
                    logger.error(f"Ошибка при выполнении {method.__name__}: {e}", exc_info=True)
                    raise e



notify_api_poller_test = NotifyApiPollerTest()