from datetime import datetime
from trueconf import Message, F, ParseMode
from service.shedule import get_upcoming_duties
from core.state import AppState
from core.database import get_db
from core.models import Duties

MD_HI = """
        🌟  Привет!  🌟

Я бот для рассылки алертов!
"""

MD_HELP = """
📋 **Основные команды:**
/help — ❓ Показать справочное сообщение
/profile — ⚙️ Дежурства и настройка уведомлений


✨ **Функции:**
• Отправить [ + ]: Добавить себя в рассылку
• Отправить [ - ]: Исключить себя из рассылки


🔗 **Ссылки:**
• [📚 Наша Grafana](https://........)
"""


MD_PROFILE = """
**Твой логин:** {}  

🗓️ **Твои ближайшие дни дежурств:**
  
{}

✨ **Напоминание:**
• Отправить [ + ]: Добавить себя в рассылку
• Отправить [ - ]: Исключить себя из рассылки
"""


async def register(state: AppState):
    if getattr(state, "_help_handler_registered", False):
        return

    @state.router.message(F.text.startswith("/help"))
    async def echo_handler(msg: Message):
        await msg.answer(MD_HI+MD_HELP, parse_mode=ParseMode.MARKDOWN)

    @state.router.message(F.text.startswith("/profile"))
    async def echo_handler(msg: Message):
        async with get_db() as db:
            # duties dates
            dates = await get_upcoming_duties(db, login=msg.author.id)
        await msg.answer(MD_PROFILE.format(msg.author.id, dates), parse_mode=ParseMode.MARKDOWN)
