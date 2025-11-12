from logging import getLogger

from aiogram import Bot

from app.schemas.notify import NewCarNotify

from ...config.config_reader import env_config


logger = getLogger(__name__)


class AdminNotifyService:
    """
    Сервис для уведомлений администраторов о новых объявлениях.
    
    Обеспечивает отправку уведомлений администраторам через Telegram бота
    при появлении новых объявлений о продаже автомобилей.
    
    Attributes:
        bot (Bot): Экземпляр Telegram бота для отправки уведомлений.
        admins_id (list[int]): Список Telegram ID администраторов.
    """
    
    def __init__(self, bot: Bot):
        """
        Инициализация сервиса уведомлений для администраторов.

        Args:
            bot (Bot): Экземпляр Telegram бота для отправки уведомлений.
            
        Example:
            >>> from aiogram import Bot
            >>> bot = Bot(token="YOUR_BOT_TOKEN")
            >>> notify_service = AdminNotifyService(bot)
        """        
        self.bot: Bot = bot
        self.admins_id: list[int] = env_config.get_admins_tg_ids
        logger.info(f"AdminNotifyService инициализирован для {len(self.admins_id)} администраторов")

    def __clip_text(self, text: str, max_length: int = 4096) -> str:
        """
        Обрезает текст до указанной максимальной длины.
        
        Если текст превышает максимальную длину, обрезает его и добавляет
        многоточие в конце.
        
        Args:
            text (str): Исходный текст для обрезки.
            max_length (int, optional): Максимальная длина текста. По умолчанию 4096.
            
        Returns:
            str: Обрезанный текст с многоточием или исходный текст.
            
        Example:
            >>> service.__clip_text("Long text here", max_length=10)
            'Long te...'
        """
        if len(text) > max_length:
            logger.debug(f"Текст обрезан с {len(text)} до {max_length} символов")
            return text[:max_length - 3] + "..."
        return text

    def __prepare_text(self, notify: NewCarNotify) -> str:
        """
        Подготавливает текст заголовка уведомления.
        
        Формирует форматированное сообщение с основной информацией
        об объявлении для отправки администратору.
        
        Args:
            notify (NewCarNotify): Объект с данными нового объявления.
            
        Returns:
            str: Отформатированный текст уведомления с HTML-разметкой.
            
        Example:
            >>> notify = NewCarNotify(advert_url="https://...", seller_phone="+123456789", analytics="...")
            >>> message = service.__prepare_text(notify)
        """
        # Убираем префикс 'tel:' из номера телефона, если он есть
        phone = str(notify.seller_phone).replace('tel:', '')
        
        return (
            f"🚗 <b>Новое объявление о продаже автомобиля</b>\n\n"
            f"🔗 <b>Ссылка:</b>\n{notify.advert_url}\n\n"
            f"📱 <b>Телефон продавца:</b>\n{phone}\n"
        )

    async def notify_admins(self, notify: NewCarNotify):
        """
        Отправляет уведомление всем администраторам о новом объявлении.
        
        Для каждого администратора отправляется два сообщения:
        1. Заголовок с основной информацией об объявлении
        2. Ответное сообщение с аналитическими данными
        
        Args:
            notify (NewCarNotify): Объект с данными нового объявления.
            
        Raises:
            Exception: Логирует ошибки отправки для каждого администратора отдельно,
                      но не прерывает процесс уведомления остальных.
                      
        Example:
            >>> notify = NewCarNotify(
            ...     advert_url="https://example.com/car",
            ...     seller_phone="+1234567890",
            ...     analytics="Detailed analytics..."
            ... )
            >>> await notify_service.notify_admins(notify)
            
        Note:
            Метод обрабатывает ошибки для каждого администратора независимо,
            что позволяет продолжить отправку остальным даже при сбое.
        """
        logger.info(f"Начало отправки уведомлений администраторам. Объявление: {notify.advert_url}")
        
        success_count = 0
        error_count = 0
        
        for admin_id in self.admins_id:
            try:
                # Формируем сообщение для отправки
                header_message = self.__prepare_text(notify)
                logger.debug(f"Отправка уведомления администратору {admin_id}")
                
                bot_msg = await self.bot.send_message(admin_id, header_message)
                
                analytics_message = (
                    f"📊 <b>Аналитика:</b>\n\n"
                    f"{self.__clip_text(notify.analytics, 3999)}\n"
                )
                await bot_msg.reply(analytics_message)
                
                success_count += 1
                logger.info(f"Уведомление успешно отправлено администратору {admin_id}")

            except Exception as e:
                error_count += 1
                logger.error(f"Ошибка при отправке уведомления администратору {admin_id}: {e}", exc_info=True)
        
        logger.info(
            f"Завершена отправка уведомлений. Успешно: {success_count}, Ошибок: {error_count}"
        )