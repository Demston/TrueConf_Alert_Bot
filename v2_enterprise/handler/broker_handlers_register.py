from core.state import AppState
from handler.broker_handlers import check_alerts


async def register_all_broker_handlers(state: AppState):
    await check_alerts.register(state)
