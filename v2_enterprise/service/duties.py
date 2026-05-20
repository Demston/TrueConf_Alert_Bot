import pandas as pd
from datetime import datetime
from settings import setting
from core.database import get_db
from core.models import Duties


def get_duties_data(source: str) -> pd.DataFrame | None:
    if source is None:
        return None

    # Old
    elif source == "excel":
        schema = {
            "Week Day": "string",
            "Date": "datetime64[ns]",
            "Main Duty": "string",
            "Additional Duty": "string",
            "Vacation": "string",
        }

        df = pd.read_excel(setting.DUTIES_FILE, dtype=schema)
        df.rename(columns={"Week Day": "DayOfWeek",
                           "Date": "Date",
                           "Main Duty": "MainDuty",
                           "Additional Duty": "AdditionalDuty",
                           "Vacation": "Vacation"}, inplace=True)
        return df

    # Current
    elif source == "db":
        with get_db() as db:
            today = str(datetime.now().date()) + ' 00:00:00.000'
            duties = db.query(Duties).filter(Duties.Date == today).first()
            if duties:
                res = {
                    "Date": duties.Date.strftime('%Y-%m-%d %H:%M:%S.000'),
                    "MainDuty": duties.LoginMain,
                    "AdditionalDuty": duties.LoginAdditional
                }
            return res

    return None


def get_today_duty(source: str):
    df = get_duties_data(source=source)

    if isinstance(df, pd.DataFrame):
        today = datetime.now().date()
        df["Date"] = pd.to_datetime(df["Date"]).dt.date
        current_duty = df[df["Date"] == today]

        main = current_duty["MainDuty"].item()
        additional = current_duty["AdditionalDuty"].item()
        return [main, additional]

    elif isinstance(df, dict):
        main = df.get("MainDuty")
        additional = df.get("AdditionalDuty")
        return [main, additional]

    return None
