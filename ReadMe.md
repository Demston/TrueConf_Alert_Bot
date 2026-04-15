## ENG. Alert system for critical system statuses. A bot for sending alerts from Grafana to TrueConf.

**The project consists of two parallel processes: main_app (the backend for data exchange between Grafana and the bot) and true_bot (the bot for alerts).**

The FastAPI-based backend application receives webhooks from Grafana. It parses these requests, formats them into a readable format, and saves event information to the log. A TrueConf bot runs in parallel, scanning the log file every few seconds and separately scanning the contact list and the on-duty list for the current date. It then sends a notification message containing the alert name and metric value (sent during business hours). A duplicate filtering system prevents spam from repeated alerts. User registration is also available; there's no need to create or delete contacts manually—everything is handled through the user-bot dialogue: you can add or remove yourself from the mailing list. Notifications come from the systems listed as primary in the Grafana header. Alerts are generated based on preset time intervals and background execution of SQL queries defined in Grafana. A separate alert is created for packages that have been running for over half an hour.

**Technologies used: Python (FastAPI + Uvicorn, Python-TrueConf-Bot, Pandas/Openpyxl), MSSQL.**

---

## RU. Система оповещений по критическим статусам систем. Бот для отправки алертов из Grafana в TrueConf. 

**Проект состоит из двух параллельно работающих процессов: main_app (бэкенд для обмена данными между Графаной и ботом) и true_bot (бот для оповещений).**

Бэкенд-приложение на базе FastAPI принимает вебхуки от Grafana. Парсит этот запрос, приводит в читабельный вид и сохраняет инфу с событием в лог. Параллельно с ним работает Труконф-бот, он раз в несколько секунд сканирует наличие лог-файла, отдельно сканирует список контактов и список дежурных на текущую дату. Далее он отправляет сообщение с оповещением: имя алерта и значение метрики (отправляет в рабочее время). Присутствует система фильтрации дублей, предотвращающая спам при повторяющихся алертах Также присутствует регистрация пользователей, заводить или удалять контакты вручную не нужно - всё делается на уровне диалога пользователя с ботом: можно как добавить себя в рассылку, так и удалить. Оповещения приходят из систем, которые перечислены в шапке нашей Графаны как основные. Оповещения генерируются на основе предустановленных интервалов времени и фонового выполнения SQL-запросов, прописанных в Графане. Отдельно создано оповещение по пакетам, которые в работе свыше получаса.

**Используемы технологии: Python (FastAPI + Uvicorn, Python-TrueConf-Bot, Pandas/Openpyxl), MSSQL.**

---

![Window](https://github.com/Demston/TrueConf_Alert_Bot/blob/main/BotScreen.png)