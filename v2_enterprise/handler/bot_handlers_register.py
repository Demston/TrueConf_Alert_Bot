from core.state import AppState
from handler.bot_handlers import help_handler, user_register


async def register_all_handlers(state: AppState):
    await help_handler.register(state)
    await user_register.register(state)
