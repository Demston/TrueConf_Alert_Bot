import os
from dotenv import load_dotenv

# Загрузка переменных из .env
load_dotenv()
# Получение данных из .env
TC_BOT_USER = os.getenv("TC_BOT_USER")
TC_BOT_PASS = os.getenv("TC_BOT_PASS")
TC_URL = os.getenv("TC_URL")  # Адрес сервера

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Папка с приложением
LOG_FILE = os.path.join(BASE_DIR, "cache", "grafana_log.txt")  # Путь к логу
CACHE_FILE = os.path.join(BASE_DIR, "cache", "sent_alerts_cache.json")  # Кэш с Джейсоном из Графаны
CONTACTS = os.path.join(BASE_DIR, "contacts", "contacts_logins.json")  # Контакты (логин и чат_ИД) инженеров для рассылки
CONTACTS_NAMES = os.path.join(BASE_DIR, "contacts", "contacts_names.json")  # Контакты (ФИО) инженеров для сопоставления с графиком дежурств
DUTIES_FILE = r'\\ПУТЬ\К\ФАЙЛУ\График.xlsx'

# График дежурств (Эксель): 'Дата' — 1-й столбец, 'Основной дежурный' — 2-й, 'в Помощь' — 3-й
COLS_INDICES = [1, 2, 3]

MORNING_TIME = '09:00:00'
EVENING_TIME = '18:00:00'


STATUS_NAMES = {
    0: "🚨",  # Ошибка
    1: "⚠️",  # Предупреждение
    2: "ℹ️",  # Информация/Статистика
    4: "✅",  # ОК
}   # Статусы сообщений
