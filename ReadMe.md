# Grafana Alerting Integration Platform for TrueConf
> **An enterprise-grade, event-driven monitoring notification system powered by FastAPI, RabbitMQ, and SQLAlchemy.**

---
[ENGLISH VERSION](#en/us) | [РУССКАЯ ВЕРСИЯ](#ru)

## [EN/US]

### 📌 Project Overview
This platform automates production incident routing by intercepting Grafana webhooks and dynamically dispatching alert payloads to active on-duty engineers via the **TrueConf** messenger corporate API. 

The project demonstrates an evolutionary path of a production-ready system, structured into two distinct historical milestones:
* **`v1_mvp/`**: The original standalone Python architecture utilizing standard filesystem pipelines, JSON datastores, and lightweight polling.
* **`v2_enterprise/`**: The modernized, asynchronous architecture migrated to an enterprise-grade message broker and fully relational database management system (RDBMS).

---

### 🏗️ Architecture & Core Design Patterns
The system operates as a single, cohesive asynchronous process optimized for low-resource footprints and ultra-low latency response times.

* **AppState (Singleton Pattern)**: Centralized container wrapping the `Bot`, `RabbitBroker`, and routing middleware. This guarantees a single, strictly controlled communication session, fully eradicating `Session is None` or race-condition network disconnects.
* **Event-Driven Broker (FastStream + RabbitMQ)**: Decouples the ingestion layer (FastAPI) from the processing layer. Webhooks are ingested instantly and offloaded to an asynchronous durable queue (`trueconf_bot_alerts`).
* **Fault Tolerance & Dead Letter Exchange (DLX)**: Integrated network resilience. If the target corporate API is temporarily unavailable, messages are gracefully rerouted to a `dlx.trueconf_bot_alerts` queue rather than being dropped or stalling the execution pipeline.
* **Automated Component Registration**: Implements decoupled runtime initialization, separating human interaction handlers (`bot_handlers`) from machine/broker ingestion workers (`broker_handlers`).

---

### 🛡️ Production Features
* **Intelligent Spam Guard**: Contextual in-memory cache throttling (`ALERTS_LAST_SEND_TIME`) that prevents duplicate alert flooding while fully respecting Grafana's specific routing repetition intervals (e.g., fast/slow channels).
* **Phantom Alert Filtering**: Built-in validation that automatically discards empty payloads or resolved updates containing zero metrics (`val == 0`) prior to generating database queries.
* **Dynamic Self-Service Registration**: Engineers can subscribe (`+` syntax) or unsubscribe (`-` syntax) directly from the messenger chat interface, automatically syncing their metadata with the database.
* **Auto-Recovery Lifecycle**: Built-in automated connection loop targeting `websockets.exceptions.InvalidStatus (HTTP 5**)` to guarantee autonomous self-healing during nightly server maintenance windows.

---

### 🛠️ Technology Stack
* **Core & Async**: Python 3.11+, FastAPI, Uvicorn, Asyncio
* **Message Broker**: RabbitMQ, FastStream
* **Database & ORM**: MSSQL, SQLAlchemy (ORM)
* **Testing**: Unittest (with Mock)

---

## [RU]

### 📌 Описание Проекта
Платформа автоматизирует маршрутизацию инцидентов промышленного мониторинга, перехватывая вебхуки Grafana и динамически рассылая оповещения дежурным инженерам через корпоративное API мессенджера **TrueConf**.

Репозиторий наглядно демонстрирует эволюцию архитектуры реального коммерческого продукта, разделенного на два этапа:
* **`v1_mvp/`**: Исходная архитектура на базе файловых очередей, JSON-справочников и периодического опроса (polling). Была успешно запущена и обкатана в промышленной эксплуатации.
* **`v2_enterprise/`**: Высоконагруженная асинхронная архитектура, переведенная на событийно-ориентированную модель, профессиональный брокер сообщений и реляционную СУБД.

---

### 🏗️ Архитектура и Паттерны Проектирования
Приложение работает в рамках единого асинхронного процесса, оптимизированного под минимальное потребление ресурсов и моментальный отклик.

* **AppState (Паттерн Синглтон)**: Глобальный контейнер, управляющий жизненным циклом экземпляров `Bot` и `RabbitBroker`. Гарантирует строгий контроль сессии связи, полностью исключая ошибки инициализации и сетевые разрывы.
* **Событийная Модель (FastStream + RabbitMQ)**: Полностью изолирует слой приема данных (FastAPI) от слоя обработки. Вебхуки мгновенно регистрируются и складываются в отказоустойчивую очередь (`trueconf_bot_alerts`).
* **Отказоустойчивость и Карман Ошибок (DLX)**: Защита от потери данных. Если корпоративный сервер временно недоступен, сообщения бережно переносятся в резервную очередь `dlx.trueconf_bot_alerts` до восстановления связи.
* **Модульная Регистрация Компонентов**: Логика разделена на два изолированных мира: хендлеры для общения с людьми (`bot_handlers`) и воркеры для обработки системных очередей (`broker_handlers`).

---

### 🛡️ Промышленные Инструменты Надежности
* **Защита от Дублирования (Антиспам)**: Контекстный кэш в оперативной памяти (`ALERTS_LAST_SEND_TIME`), который блокирует лавинообразный спам при "мигании" метрик, но четко соблюдает интервалы повторов Графаны (10/30 минут).
* **Фильтрация Фантомных Сообщений**: Встроенный барьер, отсекающий пустые алерты или уведомления со значением `0` до того, как приложение начнет нагружать СУБД тяжелыми запросами.
* **Самообслуживание и Регистрация**: Реализовано автоматическое управление подписками. Дежурные могут добавлять себя в рассылку (`+`) или удалять (`-`) прямо через чат-бот, мгновенно синхронизируя данные с СУБД.
* **Авто-Восстановление Соединения**: Бесконечный цикл удержания WebSocket-сессии с перехватом ошибок `HTTP 5**`. Бот автономно восстанавливает работу после регламентных перезагрузок сервера мессенджера.

---

### 🛠️ Используемый Стек Технологий
* **Ядро и Асинхронность**: Python 3.11+, FastAPI, Uvicorn, Asyncio
* **Брокер Сообщений**: RabbitMQ, FastStream
* **Базы Данных и ORM**: MSSQL, SQLAlchemy
* **Тестирование**: Unittest (с использованием Mock)


---

![Window](https://github.com/Demston/TrueConf_Alert_Bot/blob/main/BotScreen.png)