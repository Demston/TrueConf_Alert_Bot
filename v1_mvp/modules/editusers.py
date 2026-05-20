import json
import logging
from config import CONTACTS, CONTACTS_NAMES


def user_reg(chat_message, author_id, chat_id):
    """Registering a new contact for the mailing list / Регистрация нового контакта для рассылки"""

    chat_message = chat_message.lstrip()  # remove spaces at the beginning of the line / уберем пробелы в начале строки
    chat_message = chat_message.rstrip()  # remove spaces at the end of the line / уберем пробелы в конце строки
    # Reading a file with contacts (logins, chat_ID) / Читаем файл с контактами (логины, чат_ИД)
    try:
        if CONTACTS:
            with open(CONTACTS, 'r', encoding='utf-8') as file1:
                data1 = json.load(file1)
    # If file does not exist or is empty, create a new dictionary / Если файла нет или он пустой, создаем новый словарь
    except (FileNotFoundError, json.JSONDecodeError):
        data1 = {}
    # Reading the file with contacts (full name) / Читаем файл с контактами (ФИО)
    try:
        if CONTACTS_NAMES:
            with open(CONTACTS_NAMES, 'r', encoding='utf-8') as file2:
                data2 = json.load(file2)
    # If file does not exist or is empty, create a new dictionary / Если файла нет или он пустой, создаем новый словарь
    except (FileNotFoundError, json.JSONDecodeError):
        data2 = {}

    # Checking the user's presence / Проверяем наличие пользователя
    if chat_message[-2:] == ' +':
        user_name = chat_message[:-2]
        if author_id not in data1:
            data1[author_id] = chat_id
            # Only overwrite the file if new data has been added / Перезаписываем файл только если добавили новые данные
            with open(CONTACTS, 'w', encoding='utf-8') as file1:
                json.dump(data1, file1, ensure_ascii=False, indent=4)
            logging.info(f"Пользователь {author_id} добавлен в первый словарь")  # User {} added to the first dictionary
            # Checking the user's presence / Проверяем наличие пользователя
            if user_name not in data2:  # chat_message[:-2] - it's a name / это ФИО
                data2[chat_id] = user_name
                # Only overwrite file if new data has been added / Перезаписываем файл только если добавили новые данные
                with open(CONTACTS_NAMES, 'w', encoding='utf-8') as file2:
                    json.dump(data2, file2, ensure_ascii=False, indent=4)
                # User {} ({}) added to the second dictionary
                logging.info(f"Пользователь {author_id} ({user_name}) добавлен во второй словарь")
            # Your login {} has been added to the incident mailing list as {}
            # If you suddenly want to disable it, just send me a message
            return (f'Твой логин {author_id} добавлен в рассылку инцидентов как {user_name}\n'
                    f'Если, вдруг, захочешь её отключить, просто пришли "-"')
        else:
            # "User {} already exists, dict has not been modified
            logging.info(f"Пользователь {author_id} уже есть, справочник не изменен.")
            # UZ {} is already in the mailing list. Send a "-" if you suddenly want to disable it.
            return f'УЗ {author_id} уже есть в рассылке. Пришли "-", если, вдруг, захочешь её отключить.'

    elif chat_message == '-':
        if author_id in data1 and chat_id in data2:
            del data1[author_id]
            # Overwriting the file / Перезаписываем файл
            with open(CONTACTS, 'w', encoding='utf-8') as f:
                json.dump(data1, f, ensure_ascii=False, indent=4)
            logging.info(f"Пользователь {author_id} удален из справочника 1")  # User {} has been removed from dict 1
            fio = data2[chat_id]  # Add name to the variable / добавим ФИО в переменную, чтоб отчитаться об удалении
            del data2[chat_id]
            # Overwriting the file / Перезаписываем файл
            with open(CONTACTS_NAMES, 'w', encoding='utf-8') as f:
                json.dump(data2, f, ensure_ascii=False, indent=4)
            logging.info(f"Пользователь {author_id} ({fio}) удален из справочника 2")  # User {}{} has been removed from dict 2
            return f'УЗ {author_id} ({fio}) исключена из рассылки'  # UZ {} ({}) has been excluded from the mailing list
        else:
            logging.info(f"Пользователь {author_id} не состоит в рассылке.")  # User {} is not a member of the mailing list
            return f'УЗ {author_id} не состоит в рассылке.'  # UZ {author_id} is not a member of the mailing list

    else:
        if author_id in data1:
            logging.info(f"{data2[chat_id]}: {chat_message}")
            # (Reminder: the mailing list is disabled by the message "-")
            return f'{chat_message} © {data2[chat_id]}\n(Напоминание: рассылка отключается сообщением "-")'
        else:
            # Send "Last Name +" if you want to receive information about system incidents from Grafana.'
            # 'Please write carefully (note the case of letters and periods,
            # and leave a space between the full name and the plus sign).
            return ('Пришли "Фамилия И.О. +", если хочешь получать информацию об инцидентах систем из Графаны. '
                    'Пожалуйста, пиши внимательно (с учётом регистра букв и точек, между ФИО и плюсом - пробел).')
