import asyncio
from core.state import app_state
from core.logger import logger
from handler import bot_handlers_register, broker_handlers_register
import websockets


async def main():

    app_state.init_bot()    # bot init

    await bot_handlers_register.register_all_handlers(app_state)
    await broker_handlers_register.register_all_broker_handlers(app_state)

    logger.info("Broker is running . . .")
    asyncio.create_task(app_state.broker.start())

    logger.info("Bot is running . . .")

    while True:    # auto repair
        try:
            await app_state.trueconf_bot.run()

        except (websockets.exceptions.InvalidStatus, Exception) as e:
            logger.error(f"Connection lost (Error: {e})")
            logger.info("Next attempt after 30 seconds . . .")

            app_state.is_ready = False    # offline ready flag
            await asyncio.sleep(30)


if __name__ == "__main__":
    logger.info("Process is running . . .")
    asyncio.run(main())
