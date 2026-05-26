from core.database import get_db
from core.models import User, Duties
from core.logger import logger
from handler.bot_handlers.help_handler import MD_HI, MD_HELP
from sqlalchemy.future import select


class UserManager:
    """User registration and deletion"""

    async def process_message(self, author_id: str, chat_message: str, chat_id: str):
        async with get_db() as db:
            result = await db.execute(select(User).filter_by(ChatID=chat_id))
            user_check = result.scalars().first()

            author_id_cut = author_id.split('@')[0]
            chat_message = chat_message.strip()
            # Get user status
            user_status = user_check.IsOn if user_check else False

            # if chat_message.endswith(' +'):
            #     user_name = chat_message[:-2].strip()
            # return self._register(db, author_id, user_name, chat_id)
            if chat_message.endswith('+'):
                return await self._register(db, author_id, '', chat_id)
            elif chat_message == "-":
                return await self._delete(db, author_id, chat_id)
            elif user_status and user_status is True:
                logger.info(f"{author_id}: {chat_message}")
                return f'{chat_message} © {author_id_cut}\n\n/help - помощь\n/profile - профиль'
            else:
                return MD_HI+MD_HELP

    async def _register(self, db, author_id, user_name, chat_id):
        """User registration"""

        res_exists = await db.execute(select(User).filter_by(ChatID=chat_id))
        exists = res_exists.scalars().first()

        if exists:
            if exists.IsOn:
                logger.info(f"Пользователь {author_id} уже есть в рассылке.")
                return f'УЗ {author_id} уже есть в рассылке.\n/help - помощь\n/profile - профиль'
            else:
                exists.IsOn = True
                await db.commit()
                logger.info(f"Пользователь {author_id} уже есть, вновь включён в рассылку.")
                return (f'Твой логин {author_id} вновь включён в рассылку инцидентов как {user_name}.\n'
                        f'/help - помощь\n/profile - профиль')

        author_id_cut = author_id.split('@')[0]  # get AD login
        author_id_cut = author_id_cut.strip()
        res_duty = await db.execute(select(Duties).filter(Duties.LoginMain == author_id_cut))
        duty_record = res_duty.scalars().first()
        if duty_record:
            user_name = duty_record.Main  # get name from table
        new_user = User(Login=author_id, Name=user_name, ChatID=chat_id, IsOn=True)
        db.add(new_user)  # add user into MSSQL
        await db.commit()
        logger.warning(f'Пользователь {author_id} добавлен в рассылку как {user_name}')
        return (f'Твой логин {author_id} добавлен в рассылку инцидентов как {user_name}\n'
                f'/help - помощь\n/profile - профиль')

    async def _delete(self, db, author_id, chat_id):
        """User deletion"""

        res_exists = await db.execute(select(User).filter_by(ChatID=chat_id))
        exists = res_exists.scalars().first()

        if exists:
            exists.IsOn = False
            # db.delete(user)
            await db.commit()
            logger.warning(f"Пользователь {author_id} исключен из рассылки")
            return f'УЗ {author_id} исключена из рассылки.\n/help - помощь\n/profile - профиль'
        else:
            logger.info(f"Пользователь {author_id} не состоит в рассылке.")
            return f'УЗ {author_id} не состоит в рассылке.\n/help - помощь\n/profile - профиль'
