"""Бот для отправки алертов из Grafana дежурным инженерам.
Monitoring Bot"""

from datetime import datetime
from trueconf import Bot, Dispatcher, Router, F
from trueconf.types import Message
import asyncio
import json
from config import *
from modules.editusers import user_reg
from modules.duties import duties_today


# Экземпляры Router и Dispatcher, подключаем
r = Router()
dp = Dispatcher()
dp.include_router(r)

# Авторизация по логину и паролю
# При каждом вызове from_credentials() бот обращается к серверу за новым токеном. Срок жизни каждого токена — 1 месяц.
bot = Bot.from_credentials(
    username=TC_BOT_USER,
    password=TC_BOT_PASS,
    server=TC_URL,
    verify_ssl=False,
    dispatcher=dp
)


@r.message(F.text& ~F.from_bot) # ← Игнорировать сообщения от других ботов
async def dialog(message: Message):
    """Обмен сообщениями"""
    # print(f"От кого пришло: {message.author.id}, ChatID {message.chat_id}") # узнать логин и ID чата
    text = user_reg(message.text, message.author.id, message.chat_id) # регистрируем пользователя (или удаляем)
    await bot.send_message(message.chat_id, text)
    # await message.answer(message.text) # тест эхо-бота


async def check_alerts():
    """Отправка сообщений с алертами из файла"""
    while True:
        # Проверяем наличие данных один раз
        if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > 0:
            try:
                # Читаем и сразу чистим файл
                with open(LOG_FILE, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                open(LOG_FILE, "w").close()

                # Подготовка данных (делаем один раз для всей пачки алертов)
                duties_list = duties_today()
                if not duties_list:
                    print(f"{datetime.now().strftime('%H:%M:%S')} | [!] Список дежурных пуст. Пропускаю.")
                    continue

                with open(CONTACTS_NAMES, 'r', encoding='utf-8') as f:
                    contacts_dict = json.load(f)

                # Рассылка
                for line in lines:
                    msg = line.strip()
                    if not msg:
                        continue

                    clean_msg = msg.replace(' | ', '\n\n')

                    # Ищем, кому из дежурных отправить
                    for chat_id, user_name in contacts_dict.items():
                        if user_name in duties_list:
                            try:
                                await bot.send_message(chat_id, clean_msg)
                                # Короткий лог успеха
                                print(f"{datetime.now().strftime('%H:%M:%S')} | [OK] Отправлено для {user_name}: {msg[:30]}...")
                            except Exception as send_error:
                                print(f"{datetime.now().strftime('%H:%M:%S')} | [!] Ошибка отправки для {user_name}: {send_error}")

            except Exception as e:
                print(f"{datetime.now().strftime('%H:%M:%S')} | [!] Ошибка в check_alerts: {e}")

        # Пауза для оперативного реагирования
        await asyncio.sleep(1)


async def main():
    """Проверка файла и запуск бота"""
    asyncio.create_task(check_alerts()) # Запускаем параллельную проверку файла фоном
    await bot.run() # Запускаем бота (эхо-режим и сессия)

if __name__ == "__main__":
    print('Бот запущен . . .')
    asyncio.run(main())
