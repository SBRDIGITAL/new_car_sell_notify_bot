"""
Точка входа для запуска бота с автоматической перезагрузкой (hot reload).

Использует библиотеку hupper для автоматического перезапуска приложения
при изменении файлов исходного кода. Полезно для разработки.

Запуск:
    hupper -m hupper_main

Примечание:
    В production рекомендуется использовать main.py без hupper.
"""

import sys
from asyncio import run
from logging import INFO, basicConfig
from traceback import print_exc

from hupper import is_active, start_reloader

from app.config.config_reader import env_config
from main import main as bot_main


def setup_logging():
    """
    Настраивает логирование в зависимости от окружения.
    
    В режиме разработки (development) логи выводятся в консоль.
    В других окружениях (production) логи управляются через AppLogger.
    
    Note:
        Функция автоматически определяет окружение из конфигурации.
    """
    if env_config.env != 'development':
        basicConfig(level=INFO, stream=sys.stdout)


async def main():
    """
    Основная асинхронная функция запуска бота.
    
    Запускает основную функцию бота из main.py с обработкой ошибок:
    - KeyboardInterrupt: корректное завершение при Ctrl+C
    - Exception: логирование критических ошибок
    
    Raises:
        KeyboardInterrupt: При прерывании пользователем (Ctrl+C).
        Exception: При возникновении критических ошибок в работе бота.
        
    Example:
        >>> # Запуск через hupper
        >>> hupper -m hupper_main
    """
    try:
        await bot_main()
        
    except KeyboardInterrupt:
        print('Работа бота завершена по нажатию на Ctrl+C')
        
    except Exception:
        print('Критическая ошибка при работе бота:')
        print_exc()


if __name__ == '__main__':
    # Настраиваем логирование
    setup_logging()
    
    # Проверяем, запущен ли hupper reloader
    if is_active():
        # Hupper активен - запускаем основную функцию
        run(main())
    else:
        # Hupper не активен - запускаем reloader
        # verbose=True выводит информацию о перезагрузках в консоль
        start_reloader('hupper_main.main', verbose=True)