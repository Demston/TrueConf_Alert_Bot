import json
from config import CONTACTS, CONTACTS_NAMES


def user_reg(chat_message, author_id, chat_id):
    """Регистрация нового контакта для рассылки"""

    chat_message = chat_message.lstrip()  # уберем пробелы в начале строки
    chat_message = chat_message.rstrip()  # уберем пробелы в конце строки
    # Читаем файл с контактами (логины, чат_ИД)
    try:
        if CONTACTS:
            with open(CONTACTS, 'r', encoding='utf-8') as file1:
                data1 = json.load(file1)
    except (FileNotFoundError, json.JSONDecodeError):
        data1 = {}  # Если файла нет или он пустой, создаем новый словарь
    # Читаем файл с контактами (ФИО)
    try:
        if CONTACTS_NAMES:
            with open(CONTACTS_NAMES, 'r', encoding='utf-8') as file2:
                data2 = json.load(file2)
    except (FileNotFoundError, json.JSONDecodeError):
        data2 = {}  # Если файла нет или он пустой, создаем новый словарь

    # Проверяем наличие пользователя
    if chat_message[-2:] == ' +':
        user_name = chat_message[:-2]
        if author_id not in data1:
            data1[author_id] = chat_id
            # Перезаписываем файл только если добавили новые данные
            with open(CONTACTS, 'w', encoding='utf-8') as file1:
                json.dump(data1, file1, ensure_ascii=False, indent=4)
            print(f"Пользователь {author_id} добавлен в первый словарь")
            # Проверяем наличие пользователя
            if user_name not in data2:  # напоминаем, что chat_message[:-2] - это ФИО
                data2[chat_id] = user_name
                # Перезаписываем файл только если добавили новые данные
                with open(CONTACTS_NAMES, 'w', encoding='utf-8') as file2:
                    json.dump(data2, file2, ensure_ascii=False, indent=4)
                print(f"Пользователь {author_id} ({user_name}) добавлен во второй словарь")
            return (f'Твой логин {author_id} добавлен в рассылку инцидентов как {user_name}\n'
                    f'Если, вдруг, захочешь её отключить, просто пришли "-"')
        else:
            print(f"Пользователь {author_id} уже есть, справочник не изменен.")
            return f'УЗ {author_id} уже есть в рассылке. Пришли "-", если, вдруг, захочешь её отключить.'

    elif chat_message == '-':
        if author_id in data1 and chat_id in data2:
            del data1[author_id]
            # Перезаписываем файл
            with open(CONTACTS, 'w', encoding='utf-8') as f:
                json.dump(data1, f, ensure_ascii=False, indent=4)
            print(f"Пользователь {author_id} удален из справочника 1")
            fio = data2[chat_id]  # добавим ФИО в переменную, чтоб отчитаться об удалении
            del data2[chat_id]
            # Перезаписываем файл
            with open(CONTACTS_NAMES, 'w', encoding='utf-8') as f:
                json.dump(data2, f, ensure_ascii=False, indent=4)
            print(f"Пользователь {author_id} ({fio}) удален из справочника 2")
            return f'УЗ {author_id} ({fio}) исключена из рассылки'
        else:
            print(f"Пользователь {author_id} не состоит в рассылке.")
            return f'УЗ {author_id} не состоит в рассылке.'

    else:
        if author_id in data1:
            print(f"{data2[chat_id]}: {chat_message}")
            return f'{chat_message} © {data2[chat_id]}\n(Напоминание: рассылка отключается сообщением "-")'
        else:
            return ('Пришли "Фамилия И.О. +", если хочешь получать информацию об инцидентах систем из Графаны. '
                    'Пожалуйста, пиши внимательно (с учётом регистра букв и точек, между ФИО и плюсом - пробел).')
