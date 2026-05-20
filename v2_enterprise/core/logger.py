import logging
from logging.handlers import TimedRotatingFileHandler
import os
from datetime import datetime

LOG_DIR = "logs"


class MainFileHandler(TimedRotatingFileHandler):

    def rotation_filename(self, default_name):
        base, _sep, _suffix = default_name.partition(".")

        date = datetime.now().strftime("%Y-%m-%d")
        basepath = self.baseFilename  # e.g. /path/app.log
        dirn, fname = os.path.split(basepath)
        name_root, ext = os.path.splitext(fname)  # ('app', '.log')
        new_name = os.path.join(dirn, f"{name_root}_{date}{ext}")
        return new_name

    def doRollover(self):
        super().doRollover()


os.makedirs(LOG_DIR, exist_ok=True)
handler = MainFileHandler(
    filename=os.path.join(LOG_DIR, "TrueconfBotLog.log"),
    when="midnight",
    interval=1,
    backupCount=14,
    encoding="utf-8",
)

formatter = logging.Formatter(
        fmt='"%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s"',
        datefmt='%H:%M:%S'
    )

handler.setFormatter(formatter)

logger = logging.getLogger("Notifications")
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

logger.info("Logger started")
