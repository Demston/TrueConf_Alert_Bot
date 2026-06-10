# from typing import List, Any
# from sqlalchemy.orm import Session
from core.models import Duties, User
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

    # Extract user's full name from the User table to know who to call by "You"
    user_res = await db.execute(select(User.Name).where(User.Login == login))
    my_name = user_res.scalars().first() or ""

    # Query: main duty
    query_main = select(Duties).filter(Duties.LoginMain.like(search_login), Duties.Date >= today)
    result_main = await db.execute(query_main)
    dates_main = result_main.scalars().all()

    # Query: additional duty
    query_addit = select(Duties).filter(Duties.LoginAdditional.like(search_login), Duties.Date >= today)
    result_addit = await db.execute(query_addit)
    dates_addit = result_addit.scalars().all()

    # Sorting dates (DB objects)
    duties_main = sorted(dates_main, key=lambda x: x.Date if x.Date else today)
    duties_addit = sorted(dates_addit, key=lambda x: x.Date if x.Date else today)

    # Formatting the main duty part
    lines_main = []
    for duty in duties_main:
        if not duty.Date:
            continue
        date_str = duty.Date.strftime('%d.%m.%Y')

        day_name = duty.WeekDay if duty.WeekDay else "??"

        # Determine who is "You" and who is your partner
        partner = duty.Additional if duty.Additional else "Not assigned"
        name_block = f"You + {partner}" if duty.Main == my_name else f"{duty.Main} + {partner}"
        lines_main.append(f"    {date_str} | {day_name}  ({name_block})")

    # Formatting the additional duty part
    lines_addit = []
    for duty in duties_addit:
        if not duty.Date:
            continue
        date_str = duty.Date.strftime('%d.%m.%Y')

        day_name = duty.WeekDay if duty.WeekDay else "??"

        # Determine who is "You" and who is your partner
        partner = duty.Main if duty.Main else "Not assigned"
        name_block = f"{partner} + You" if duty.Additional == my_name else f"{partner} + {duty.Additional}"
        lines_addit.append(f"    {date_str} | {day_name}  ({name_block})")

    main_line = "\n".join(lines_main) if lines_main else "    There are no scheduled shifts."
    addit_line = "\n".join(lines_addit) if lines_addit else "    There are no scheduled shifts."

    return f'🔴 **Main duty:**\n{main_line}\n\n🔵 **Additional:**\n{addit_line}'
