# from typing import List, Any
# from sqlalchemy.orm import Session
from core.models import Duties
from datetime import datetime
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_upcoming_duties(db: Session, login: str) -> str:
    """
    Searches the database for all future on-call dates for the specified login.
    Returns a sorted list of strings with dates in DD/MM/YYYY format.
    """
    search_login = f"{login.partition('@')[0]}%"
    today = datetime.now().date()
    print(today)

    # query: main duty
    query_main = select(Duties).filter(Duties.LoginMain.like(search_login), Duties.Date >= today)
    result_main = await db.execute(query_main)
    dates_main = result_main.scalars().all()

    # query: additional duty
    query_addit = select(Duties).filter(Duties.LoginAdditional.like(search_login), Duties.Date >= today)
    result_addit = await db.execute(query_addit)
    dates_addit = result_addit.scalars().all()

    # Collecting and sorting dates
    dates_main_list = [duty.Date.strftime('%d.%m.%Y') for duty in dates_main if duty.Date]
    dates_main_list.sort()
    dates_main_line = "\n".join([f"    {date}" for date in dates_main_list])

    dates_addit_list = [duty.Date.strftime('%d.%m.%Y') for duty in dates_addit if duty.Date]
    dates_addit_list.sort()
    dates_addit_line = "\n".join([f"    {date}" for date in dates_addit_list])

    return f'Main duty officer:\n{dates_main_line}\nAdditional:\n{dates_addit_line}'
