import asyncio
from core.state import AppState
from core.logger import logger
from handler import bot_handlers_register, broker_handlers_register
import websockets


async def main():

    # bot init
    app = AppState()
    app.init_bot()

    await bot_handlers_register.register_all_handlers(app)
    await broker_handlers_register.register_all_broker_handlers(app)

    logger.info("Broker is running . . .")
    asyncio.create_task(app.broker.start())     # запускаем в фоне

    logger.info("Bot is running . . .")
    # auto repair
    while True:
        try:
            await app.trueconf_bot.run()

        except (websockets.exceptions.InvalidStatus, Exception) as e:
            logger.error(f"Connection lost (Error: {e})")
            logger.info("Next attempt after 30 seconds . . .")

            app.is_ready = False    # offline ready flag
            await asyncio.sleep(30)


if __name__ == "__main__":
    logger.info("Process is running . . .")
    asyncio.run(main())
