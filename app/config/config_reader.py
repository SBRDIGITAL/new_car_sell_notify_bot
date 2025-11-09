"""Config reader using pydantic-settings.

Этот модуль показывает, как читать переменные окружения и `.env` файл
в кодировке UTF-8 с помощью `pydantic-settings` (совместимо с pydantic v2).

Usage:
    from app.config.config_reader import get_settings

    settings = get_settings()
    host = settings.redis_host

Файлы `.env` будут прочитаны автоматически в кодировке UTF-8 благодаря
параметру `env_file_encoding` в `SettingsConfigDict`.
"""
from __future__ import annotations

from functools import lru_cache
from typing import Optional

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings read from environment / .env (UTF-8).

    Добавляйте сюда поля, которые нужны приложению. По умолчанию значения
    будут браться из переменных окружения, а при отсутствии — использовать
    значения по умолчанию, указанные ниже.
    """
    # Bot
    bot_token: SecretStr = Field(SecretStr(''), env="BOT_TOKEN")
    admins_tg_ids: str = Field('', env="ADMIN_TG_IDS")

    # Notify API
    notify_api_host: str = Field("localhost", env="NOTIFY_API_HOST")
    notify_api_port: int = Field(8000, env="NOTIFY_API_PORT")

    # Дополнительные настройки
    env: str = Field("development", env="ENV")

    # pydantic-settings configuration: указываем .env и кодировку UTF-8
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        populate_by_name=True,
        # можно добавить другие опции при необходимости
    )

    @classmethod
    def check_bot_token(cls):
        """
        ## Проверяет наличие токена бота.

        Raises:
            ValueError: Ошибка, если не указан токен бота.
        """        
        if not cls.bot_token.get_secret_value():
            raise ValueError('Не указан токен бота, обратитесь к @BotFather')

    @property
    def get_admins_tg_ids(self) -> list[int]:
        """
        ## Возвращает список `telegram_id` администраторов.

        Returns:
            list[int]: Список `telegram_id` администраторов.
        """        
        return [
            int(id_str) for id_str in self.admins_tg_ids.split(",") \
                if id_str.strip()
            ]


@lru_cache()
def get_settings() -> Settings:
    """Возвращает кешированный экземпляр `Settings`.

    lru_cache обеспечивает, что настройки будут прочитаны один раз при
    первом вызове и потом переиспользоваться (удобно для FastAPI зависимостей).
    """

    return Settings()

env_config = get_settings()
env_config.check_bot_token()

__all__ = ["Settings", "get_settings", "env_config"]