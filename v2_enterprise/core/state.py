from dataclasses import dataclass, field
from typing import Optional
from trueconf import Bot, Router, Dispatcher
from faststream.rabbit import RabbitBroker, RabbitQueue
from settings import setting


@dataclass
class AppState:
    """Global State"""

    trueconf_bot: Optional[Bot] = None
    broker: Optional[RabbitBroker] = None
    is_ready: bool = False
    main_rabbit_queue: Optional[RabbitQueue] = None
    router: Optional[Router] = None
    dp: Optional[Dispatcher] = None
    
    def is_initialized(self) -> bool:
        return self.trueconf_bot is not None and self.broker is not None
    
    def init_bot(self):
        try:
            self.router = Router()
            self.dp = Dispatcher()
            self.dp.include_router(self.router)

            self.trueconf_bot = Bot.from_credentials(
                username=setting.TC_BOT_USER,
                password=setting.TC_BOT_PASS,
                server=setting.TC_URL,
                verify_ssl=False,
                dispatcher=self.dp
                )   
            
            self.broker = RabbitBroker(setting.rabbit_mq_connection_string)
            self.main_rabbit_queue =  RabbitQueue(name="trueconf_bot_alerts", durable=True,
                                                  arguments={"x-dead-letter-exchange": "dlx.trueconf_bot_alerts",})

            self.is_ready = True
        except Exception as e:
            raise Exception(e)


app_state = AppState()
