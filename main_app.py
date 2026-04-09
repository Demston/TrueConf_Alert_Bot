"""Backend для приёма алертов от Grafana для последующей рассылки TrueConf-ботом."""

from datetime import datetime
from fastapi import FastAPI, Request
from config import *
from modules.grafanabuffer import load_cache, save_cache


app = FastAPI()


@app.post("/webhook/grafana")
async def handle_grafana(request: Request):
    """Принимаем и сохраняем данные из графаны в читабельном виде (в файл) для последующей отправки ботом"""
    data = await request.json()
    cur_time = datetime.now().strftime('%H:%M:%S')
    timestamp = datetime.now().strftime('%H:%M')

    if MORNING_TIME < cur_time < EVENING_TIME:

        alerts = data.get('alerts', [])
        # Загружаем json из файла
        sent_alerts = load_cache()

        for alert in alerts:
            status = alert.get('status')
            fingerprint = alert.get('fingerprint')
            alert_name = alert.get('labels', {}).get('alertname', 'Алерт')

            if status != 'firing':
                # Обновим кэш на resolved, чтобы потом сработал новый firing
                sent_alerts[fingerprint] = status
                save_cache(sent_alerts)
                continue  # пропускаем, если это не алёрт

            # Проверка кэша
            now_ts = datetime.now().timestamp()
            last_send_time = sent_alerts.get(f"{fingerprint}_last_ts", 0)

            # Если статус тот же и прошло меньше 9 минут — игнорим
            # Это не даст заспамить десятком сообщений сразу, но пропустит повтор через 10 минут
            if sent_alerts.get(fingerprint) == 'firing' and (now_ts - last_send_time < 540):
                continue

            # Если прошли — обновляем кэш и время
            sent_alerts[fingerprint] = status
            sent_alerts[f"{fingerprint}_last_ts"] = now_ts
            save_cache(sent_alerts)

            # Парсим
            values = alert.get('values') or {}  # Вытаскиваем только имя и цифру
            val = values.get('B', values.get('A', 0))  # Пробуем взять B (Reduce) или A (SQL), если пусто — 0
            if val == 0:
                continue  # Пропускаем алёрт нулём и идем дальше по циклу

            # Формируем строку с алёртом
            full_message = f"{timestamp} {alert_name}:  {val}"

            # Запись в лог-файл (бот увидит одну строку и сразу отправит)
            log_line = full_message.replace('\n', ' | ')  # разделитель для записи в лог
            with open(LOG_FILE, 'a', encoding='utf-8') as f:
                f.write(log_line + "\n")
                f.flush()  # сбросить данные из памяти на диск прямо сейчас

            print(f"{cur_time}, {log_line}")

    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
