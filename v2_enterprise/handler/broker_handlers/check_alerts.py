from datetime import datetime, time
from core.state import AppState
import json
from trueconf import ParseMode
from service.duties import get_today_duty
from core.database import get_db
from core.models import User
from settings import setting
from core.logger import logger


# Словарь для таймингов (антиспам)
ALERTS_LAST_SEND_TIME = {}

async def register(state: AppState):
    if getattr(state, "_check_alerts_broker_registered", False):
        return

    @state.broker.subscriber(queue=state.main_rabbit_queue,  no_ack=False)
    async def task_handler(msg):

        current_time = datetime.now().time()
        if not (time(9, 0) <= current_time <= time(18, 0)): # Рабочее ли время (9-18ч.)
            return

        timestamp = datetime.now().strftime('%H:%M')

        # if not state.is_ready:
        #     return
        # если бот подключен — принудительно оживляем флаг для системы
        state.is_ready = True

        # msg = json.loads(msg) # не нужно, уже - словарь
        full_message = ''
        alerts = msg.get('alerts', [])
        for alert in alerts:
            # status = alert.get('status')
            fingerprint = alert.get('fingerprint')
            alert_name = alert.get('labels', {}).get('alertname', 'Алерт')
            values = alert.get('values') or {} # Вытаскиваем только имя и цифру
            val = values.get('B', values.get('A', 0)) # Пробуем взять B (Reduce) или A (SQL), если пусто — 0
            if val == 0:
                continue  # Пропускаем алёрт нулём и идем дальше по циклу

            # фильтр от спама
            now_ts = datetime.now().timestamp()
            # Если этот алёрт уже уходил меньше заданного интервала назад (указываем в секундах) — скипаем его повтор
            if fingerprint in ALERTS_LAST_SEND_TIME and (now_ts - ALERTS_LAST_SEND_TIME[fingerprint] < 120):
                continue
            ALERTS_LAST_SEND_TIME[fingerprint] = now_ts  # запоминаем время отправки

            # Формируем строку с алёртом
            full_message = f"{timestamp} {alert_name}:  {val}"

        if not full_message:  # Периодически прилетают пустые фантомные сообщения
            return  # Если все алерты пустые, дальше не идем

        duties_list = get_today_duty(source="db")  # excel or db
        if not duties_list:
            return  # Безопасно завершим, чтобы не плодить очередь

        # with open(setting.CONTACTS_NAMES, 'r', encoding='utf-8') as f:
        #     contacts_dict = json.load(f)       # старый вариант

        duties_list_id = []
        for dut in duties_list:
            # Если None или пустота — скипаем
            if not dut:
                continue
            with get_db() as db:
                chat_id = db.query(User.ChatID).filter(User.Login.like(dut+'%')).scalar()
                if chat_id:
                    duties_list_id.append(str(chat_id))

        # for chat_id, user_name in contacts_dict.items():
        #   if user_name in duties_list:  # старый вариант

        for chat_id in duties_list_id:
            try:
                await state.trueconf_bot.send_message(
                        chat_id=chat_id,
                        text=full_message,
                        parse_mode=ParseMode.MARKDOWN
                    )
            except Exception as send_error:
                logger.error(f" {send_error}")
