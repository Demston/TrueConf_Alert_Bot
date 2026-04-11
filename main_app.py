"""Backend for receiving alerts from Grafana for subsequent distribution by the TrueConf bot. /
Backend для приёма алертов от Grafana для последующей рассылки TrueConf-ботом."""

from datetime import datetime
from fastapi import FastAPI, Request
from config import *
from modules.grafanabuffer import load_cache, save_cache


app = FastAPI()


@app.post("/webhook/grafana")
async def handle_grafana(request: Request):
    """Receive and save data from Grafana in a readable form (in a file) for subsequent sending by the bot /
    Принимаем и сохраняем данные из графаны в читабельном виде (в файл) для последующей отправки ботом"""
    data = await request.json()
    cur_time = datetime.now().strftime('%H:%M:%S')
    timestamp = datetime.now().strftime('%H:%M')

    if MORNING_TIME < cur_time < EVENING_TIME:

        alerts = data.get('alerts', [])
        # Loading JSON from a file / Загружаем json из файла
        sent_alerts = load_cache()

        for alert in alerts:
            status = alert.get('status')
            fingerprint = alert.get('fingerprint')
            alert_name = alert.get('labels', {}).get('alertname', 'Алерт')

            if status != 'firing':
                # Let's update the cache to resolved so that the new firing will work later. /
                # Обновим кэш на resolved, чтобы потом сработал новый firing
                sent_alerts[fingerprint] = status
                save_cache(sent_alerts)
                continue  # skip if it's not an alert / пропускаем, если это не алёрт

            # Checking the cache / Проверка кэша
            now_ts = datetime.now().timestamp()
            last_send_time = sent_alerts.get(f"{fingerprint}_last_ts", 0)

            # If the status is the same and less than 2 minutes have passed, ignore it.
            # This will prevent you from spamming them with dozens of messages at once,
            # but will allow you to see a repeat after 2 minutes. /
            # Если статус тот же и прошло меньше 2 минут — игнорим
            # Это не даст заспамить десятком сообщений сразу, но пропустит повтор через 2 минуты
            if sent_alerts.get(fingerprint) == 'firing' and (now_ts - last_send_time < 120):
                continue

            # If you've passed, update the cache and time./ Если прошли — обновляем кэш и время
            sent_alerts[fingerprint] = status
            sent_alerts[f"{fingerprint}_last_ts"] = now_ts
            save_cache(sent_alerts)

            # Parsing / Парсинг
            values = alert.get('values') or {}  # Вытаскиваем только имя и цифру
            val = values.get('B', values.get('A', 0))  # Пробуем взять B (Reduce) или A (SQL), если пусто — 0
            # Skip the alert with zero and move on through the cycle. / Пропускаем алёрт с нулём и идем дальше по циклу
            if val == 0:
                continue

            # Creating a line with an alert / Формируем строку с алёртом
            full_message = f"{timestamp} {alert_name}:  {val}"

            # Write to a log file (the bot will see one line and send it immediately) /
            # Запись в лог-файл (бот увидит одну строку и сразу отправит)
            log_line = full_message.replace('\n', ' | ')  # separator for the log / разделитель для лога
            with open(LOG_FILE, 'a', encoding='utf-8') as f:
                f.write(log_line + "\n")
                f.flush()  # сбросить данные из памяти на диск прямо сейчас

            print(f"{cur_time}, {log_line}")

    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
