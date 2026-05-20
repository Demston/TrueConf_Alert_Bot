import os
from dotenv import load_dotenv

# Loading variables from .env / Загрузка переменных из .env
load_dotenv()
# Getting data from .env / Получение данных из .env
TC_BOT_USER = os.getenv("TC_BOT_USER")
TC_BOT_PASS = os.getenv("TC_BOT_PASS")
TC_URL = os.getenv("TC_URL")  # Server address / Адрес сервера

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Application folder / Папка с приложением

LOG_FILE = os.path.join(BASE_DIR, "cache", "grafana_cache.txt")  # Path to the log / Путь к логу

# Cash with Jason from Grafana / Кэш с Джейсоном из Графаны
CACHE_FILE = os.path.join(BASE_DIR, "cache", "sent_alerts_cache.json")

# Engineers' login and chat ID for mailing lists / Логин и чат_ИД инженеров для рассылки
CONTACTS = os.path.join(BASE_DIR, "contacts", "contacts_logins.json")

# Full names of engineers for comparison with the duty schedule / ФИО инженеров для сопоставления с графиком дежурств
CONTACTS_NAMES = os.path.join(BASE_DIR, "contacts", "contacts_names.json")

DUTIES_FILE = r'\\ПУТЬ\К\ФАЙЛУ\График.xlsx'  # Duty schedule file

# Duty schedule (Excel): 'Date' is the 1st column, 'Main duty officer' is the 2nd, 'Help' is the 3rd /
# График дежурств (Эксель): 'Дата' — 1-й столбец, 'Основной дежурный' — 2-й, 'в Помощь' — 3-й
COLS_INDICES = [1, 2, 3]

MORNING_TIME = '09:00:00'
EVENING_TIME = '18:00:00'


STATUS_NAMES = {
    0: "🚨",
    1: "⚠️",
    2: "ℹ️",
    4: "✅",
}   # Message statuses / Статусы сообщений (Not using now)
