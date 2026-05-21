from core.database import get_db
from core.models import User, Duties
from core.logger import logger
from handler.bot_handlers.help_handler import MD_HI, MD_HELP


class UserManager:
    """User registration and deletion"""

    def process_message(self, author_id: str, chat_message: str, chat_id: str):
        with get_db() as db:
            user_check = db.query(User).filter_by(ChatID=chat_id).first()

            author_id_cut = author_id.split('@')[0]
            chat_message = chat_message.strip()
            # Get user status
            user_status = user_check.IsOn if user_check else False

            # if chat_message.endswith(' +'):
            #     user_name = chat_message[:-2].strip()
            # return self._register(db, author_id, user_name, chat_id)
            if chat_message.endswith('+'):
                return self._register(db, author_id, '', chat_id)
            elif chat_message == "-":
                return self._delete(db, author_id, chat_id)
            elif user_status and user_status is True:
                logger.info(f"{author_id}: {chat_message}")
                return f'{chat_message} © {author_id_cut}\n\n/help - помощь\n/profile - профиль'
            else:
                return MD_HI + MD_HELP

    def _register(self, db, author_id, user_name, chat_id):
        """User registration"""

        exists = db.query(User).filter_by(ChatID=chat_id).first()
        if exists:
            if exists.IsOn:
                logger.info(f"Пользователь {author_id} уже есть в рассылке.")
                return f'УЗ {author_id} уже есть в рассылке.\n/help - помощь\n/profile - профиль'
            else:
                exists.IsOn = True
                db.commit()
                logger.info(f"Пользователь {author_id} уже есть, вновь включён в рассылку.")
                return (f'Твой логин {author_id} вновь включён в рассылку инцидентов как {user_name}.\n'
                        f'/help - помощь\n/profile - профиль')

        author_id_cut = author_id.split('@')[0]  # возьмем AD-логин
        author_id_cut = author_id_cut.strip()
        duty_record = db.query(Duties).filter(Duties.LoginMain == author_id_cut).first()
        if duty_record:
            user_name = duty_record.Main  # get name from table
        new_user = User(Login=author_id, Name=user_name, ChatID=chat_id, IsOn=True)
        db.add(new_user)  # add user into MSSQL
        db.commit()
        logger.warning(f'Пользователь {author_id} добавлен в рассылку как {user_name}')
        return (f'Твой логин {author_id} добавлен в рассылку инцидентов как {user_name}\n'
                f'/help - помощь\n/profile - профиль')

    def _delete(self, db, author_id, chat_id):
        """User deletion"""

        exists = db.query(User).filter_by(ChatID=chat_id).first()
        if exists:
            exists.IsOn = False
            # db.delete(user)
            db.commit()
            logger.warning(f"Пользователь {author_id} исключен из рассылки")
            return f'УЗ {author_id} исключена из рассылки.\n/help - помощь\n/profile - профиль'
        else:
            logger.info(f"Пользователь {author_id} не состоит в рассылке.")
            return f'УЗ {author_id} не состоит в рассылке.\n/help - помощь\n/profile - профиль'
