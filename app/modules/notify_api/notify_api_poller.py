from .notify_api_client import NotifyApiClient



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

    async def get_new_notifies(self):
        pass
    

notify_api_poller = NotifyApiPoller()