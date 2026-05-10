"""A bot for sending alerts from Grafana to on-duty engineers. /
Бот для отправки алертов из Grafana дежурным инженерам.
---Monitoring Bot---"""

from datetime import datetime
from trueconf import Bot, Dispatcher, Router, F
from trueconf.types import Message
import asyncio
import json
from config import *
from modules.editusers import user_reg
from modules.duties import duties_today
import logging


# Logging settings
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs\\bot.log"),  # to file
        logging.StreamHandler()          # to console
    ]
)


# Router and Dispatcher instances, connect / Экземпляры Router и Dispatcher, подключаем
r = Router()
dp = Dispatcher()
dp.include_router(r)

# Authorization by login and password. The lifespan of each token is 1 month. / Авторизация по логину и паролю
# При каждом вызове from_credentials() бот обращается к серверу за новым токеном. Срок жизни каждого токена — 1 месяц.
bot = Bot.from_credentials(
    username=TC_BOT_USER,
    password=TC_BOT_PASS,
    server=TC_URL,
    verify_ssl=False,
    dispatcher=dp
)


@r.message(F.text& ~F.from_bot)  # ← Ignore messages from other bots / Игнорировать сообщения от других ботов
async def dialog(message: Message):
    """Messaging / Обмен сообщениями"""
    # print(f"От кого пришло: {message.author.id}, ChatID {message.chat_id}") # find out the login and chat ID
    text = user_reg(message.text, message.author.id, message.chat_id)  # register a user (or delete)
    await bot.send_message(message.chat_id, text)
    # await message.answer(message.text) # Echobot test


async def check_alerts():
    """Sending alert messages from a file / Отправка сообщений с алертами из файла"""
    while True:
        # Check the availability of data once / Проверяем наличие данных один раз
        if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > 0:
            try:
                # We read and immediately clean the file / Читаем и сразу чистим файл
                with open(LOG_FILE, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                open(LOG_FILE, "w").close()

                # Data preparation (we do this once for the entire batch of alerts) /
                # Подготовка данных (делаем один раз для всей пачки алертов)
                duties_list = duties_today()
                if not duties_list:
                    logging.info(f"{datetime.now().strftime('%H:%M:%S')} | [!] Список дежурных пуст. Пропускаю.")
                    continue

                with open(CONTACTS_NAMES, 'r', encoding='utf-8') as f:
                    contacts_dict = json.load(f)

                # Sending messages / Рассылка
                for line in lines:
                    msg = line.strip()
                    if not msg:
                        continue

                    clean_msg = msg.replace(' | ', '\n\n')

                    # We are looking for someone on duty to send / Ищем, кому из дежурных отправить
                    for chat_id, user_name in contacts_dict.items():
                        if user_name in duties_list:
                            try:
                                await bot.send_message(chat_id, clean_msg)
                                # Short success log / Короткий лог успеха
                                logging.info(f"{datetime.now().strftime('%H:%M:%S')} | [OK] Send to {user_name}: {msg[:30]}...")
                            except Exception as send_error:
                                logging.info(f"{datetime.now().strftime('%H:%M:%S')} | [!] Error sending for {user_name}: {send_error}")

            except Exception as e:
                logging.info(f"{datetime.now().strftime('%H:%M:%S')} | [!] Error in check_alerts: {e}")

        # Pause for rapid response / Пауза для оперативного реагирования
        await asyncio.sleep(1)


async def main():
    """Checking the file and running the bot / Проверка файла и запуск бота"""
    asyncio.create_task(check_alerts())  # Run a parallel file in the background / Запускаем проверку файла фоном
    await bot.run()  # Launching the bot (echo mode and session) / Запускаем бота (эхо-режим и сессия)

if __name__ == "__main__":
    logging.info('Bot is running . . .')
    asyncio.run(main())
