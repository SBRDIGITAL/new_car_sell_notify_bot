from ...utils.aiohttp_client.aiohttp_client import AiohttpClient
from ...config.config_reader import env_config



class NotifyApiClient:

    def __init__(self, api_version: int = 1):
        """
        ## Инициализация поллера.
        
        Args:
            api_version: Версия API для использования (по умолчанию 1).

        Attributes:
            api_version (str): Версия API в формате строки (например, '/v1/').
            api_base_url (str): Базовый URL для подключения к API.
            client (AiohttpClient): Асинхронный HTTP-клиент для выполнения запросов.
            lifecheck (str): Ендпоинт для проверки состояния сервиса.
            notify (str): Ендпоинт для работы с уведомлениями.
        """
        self.api_version = f'/v{api_version}/'
        self.api_base_url = self._create_api_base_url
        self.client = AiohttpClient(base_url=self.api_base_url)
        # Ендпоинты:
        self.lifecheck = 'lifecheck'
        self.notify = 'notify'
    
    async def __aenter__(self):
        """Вход в асинхронный контекстный менеджер."""
        await self.client.__aenter__()
        return self
    
    async def __aexit__(self, *args):
        """Выход из асинхронного контекстного менеджера."""
        await self.client.__aexit__(*args)

    @property
    def _create_api_base_url(self) -> str:
        """
        ## Формирует базовый URL для подключения к API.
        
        Создаёт полный URL для доступа к API сервиса уведомлений,
        включая хост, порт и версию API из конфигурации.
        
        :return: Полный базовый URL API (например, "http://localhost:8000/v1/").
        """
        # Ранее была ошибка: две подряд стоящие скобки после строк
        # приводили к попытке вызвать строку как функцию:
        #   ("http://host") (":8000")  -> TypeError: 'str' object is not callable
        # Формируем URL корректно через одну f-строку.
        return (
            f"http://{env_config.notify_api_host}"
            f":{env_config.notify_api_port}"
            f"{self.api_version}"
        )
    
    async def _run_lifecheck(self):
        """
        ## Выполняет запрос к эндпоинту проверки состояния сервиса. 
        
        Returns:
            tuple (): Кортеж, который содержит data, status, headers
        """
        return await self.client.get(self.lifecheck)

    async def _create_notify(self, json: dict):
        """
        ## Выполняет запрос к эндпоинту создания уведомления.
        
        Args:
            json (dict): Данные уведомления в формате словаря.
        """
        return await self.client.post(self.notify, json=json)
    
    async def _get_new_notifies(self):
        """
        ## Выполняет запрос к эндпоинту получения новых уведомлений.
        
        Returns:
            tuple (): Кортеж, который содержит data, status, headers
        """
        return await self.client.get(self.notify)