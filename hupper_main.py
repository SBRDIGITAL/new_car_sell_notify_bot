import sys

from logging import (
    basicConfig,
    INFO
)

from asyncio import run
from traceback import print_exc

from hupper import is_active, start_reloader

from app.config.config_reader import env_config

from main import main as main_from_main_py


# Настройка логирования в консоль только если НЕ в Docker
# В Docker логи пишутся через AppLogger в файлы, если окружение не для разработки
if env_config.env != 'development':
    basicConfig(level=INFO, stream=sys.stdout)



if __name__ == '__main__':
    async def main():
        """
        ## Чтобы запустить, используй в консоли команду:

        ### Run
            ```bash
            hupper -m hupper_main
            ```
        """
        try:
            await main_from_main_py()
            
        except KeyboardInterrupt:
            print('Работа бота завершена по нажатию на ctrl + c')
            # app_logger.info('Работа бота завершена по нажатию на ctrl + c')
            
        except Exception as ex:
            print_exc()
            # app_logger.exception('Критическая ошибка', exc_info=ex)
            
    if is_active():
        run(main())
    else:
        start_reloader('hupper_main.main', verbose=True)  # Указываем полный путь к функции