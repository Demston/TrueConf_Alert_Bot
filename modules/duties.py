import pandas as pd
from datetime import datetime
from config import DUTIES_FILE, COLS_INDICES
import logging
# The openpyxl library is required, pandas calls it. / Обязательно нужна библиотека openpyxl, pandas обращается к ней

duties_date, emp_main, emp_assistant = 'duties_date', 'emp_main', 'emp_assistant'

# Read the required columns / Читаем нужные столбцы
df = pd.read_excel(
    DUTIES_FILE,
    usecols=COLS_INDICES,  # Take columns by numbers (you can also use names) / Столбцы по номерам (можно и по именам)
    header=0,              # Skip the first line / Пропускаем первую строку
    names=[duties_date, emp_main, emp_assistant],  # Once by numbers - any names / Раз по номерам - любые имена
    engine='openpyxl'
)


def duties_today():
    """Find out who is on duty and return the list. / Узнаем, кто дежурный, возвращает список"""
    # Переводим столбец с датой в формат datetime, чтобы не было проблем со сравнением
    df[duties_date] = pd.to_datetime(df[duties_date]).dt.date

    # Get people on duty for today. / Берем дежурных на сегодня
    today = datetime.now().date()
    current_duty = df[df[duties_date] == today]

    if not current_duty.empty:
        first = current_duty.iloc[0][emp_main]
        second = current_duty.iloc[0][emp_assistant]
        logging.info(f"Сегодня дежурят: {first} и {second}")  # On duty today
        return [first, second]
    else:
        logging.info("Сегодня никто не дежурит.")  # There is no one on duty today.
        return []
