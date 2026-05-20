from trueconf import Message, F
from core.state import AppState


async def register(state: AppState):
    if getattr(state, "_echo_registered", False):
        return
    
    @state.router.message(F.text)
    async def echo_handler (msg: Message):
        await msg.answer(f"Эхо : {msg.text}")
