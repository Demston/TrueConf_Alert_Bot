from datetime import datetime, time
from core.state import AppState
import json
from settings import setting
from trueconf import ParseMode
from service.duties import get_today_duty
from core.database import get_db
from core.models import User
from core.logger import logger
from sqlalchemy.future import select


# antispam dict
ALERTS_LAST_SEND_TIME = {}


async def register(state: AppState):
    if getattr(state, "_check_alerts_broker_registered", False):
        return

    @state.broker.subscriber(queue=state.main_rabbit_queue,  no_ack=False)
    async def task_handler(msg):

        current_time = datetime.now().time()
        if not (time(9, 0) <= current_time <= time(18, 0)):     # work time (9-18)
            return
        timestamp = datetime.now().strftime('%H:%M')

        # if not state.is_ready:
        #     return
        # if bot online - repair's flag for system
        state.is_ready = True

        # msg = json.loads(msg)
        alert_lines = []
        alerts = msg.get('alerts', [])

        for alert in alerts:
            # status = alert.get('status')
            fingerprint = alert.get('fingerprint', 'default_key')
            alert_name = alert.get('labels', {}).get('alertname', 'Алерт')
            values = alert.get('values') or {}  # get num only
            val = values.get('B', values.get('A', 0))  # get B (Reduce) or A (SQL), 0 if empty
            if val == 0:
                continue  # skip 0-alert

            # antispam filter
            now_ts = datetime.now().timestamp()
            # If this alert has already gone less than specified interval back (in seconds) - skip it
            if fingerprint in ALERTS_LAST_SEND_TIME and (now_ts - ALERTS_LAST_SEND_TIME[fingerprint] < 120):
                continue
            ALERTS_LAST_SEND_TIME[fingerprint] = now_ts  # remember send time

            alert_lines.append(f"{timestamp} {alert_name}: {val}")

        # final string with alert
        full_message = "\n".join(alert_lines)

        if not full_message:  # if empty
            return

        duties_list = await get_today_duty(source="db")  # excel or db
        if not duties_list:
            return

        # with open(setting.CONTACTS_NAMES, 'r', encoding='utf-8') as f:
        #     contacts_dict = json.load(f)       # old
        duties_list_id = []
        async with get_db() as db:
            for dut in duties_list:

                if not dut:
                    continue
                search_mask = f"{dut}%"
                query = select(User.ChatID).where(User.Login.like(search_mask))
                result = await db.execute(query)
                chat_id = result.scalars().first()

                if chat_id:
                    duties_list_id.append(str(chat_id))

        # for chat_id, user_name in contacts_dict.items():
        #   if user_name in duties_list:  # old
        for chat_id in duties_list_id:
            try:
                await state.trueconf_bot.send_message(
                        chat_id=chat_id,
                        text=full_message,
                        parse_mode=ParseMode.MARKDOWN
                    )
            except Exception as send_error:
                logger.error(f" {send_error}")
