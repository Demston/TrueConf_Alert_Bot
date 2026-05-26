from trueconf import Message, F
from core.state import AppState
from service.user_manager import *
# from service.register import user_reg


async def register(state: AppState):
    if getattr(state, "_user_register_registered", False):
        return

    @state.router.message(F.text)
    async def dialog(message: Message):
        """Messaging"""
        # print(f"От кого пришло: {message.author.id}, ChatID {message.chat_id}") # look login and chat ID
        text = await UserManager().process_message(message.author.id, message.text, message.chat_id)
        # text = user_reg(message.text, message.author.id, message.chat_id)  # user registration (or deletion)
        await state.trueconf_bot.send_message(message.chat_id, text)
