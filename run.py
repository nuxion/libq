import logging
import sys
from logging import config
from typing import Any, Dict

from rich.logging import RichHandler

from libq.worker import AsyncWorker

LOG_CONFIG: Dict[str, Any] = dict(  # no cov
    version=1,
    disable_existing_loggers=False,
    loggers={
        "libq": {"level": "DEBUG", "handlers": ["rich"]},
    },
    handlers={
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": sys.stdout,
        },
        "rich": {"class": "rich.logging.RichHandler"},
    },
    formatters={
        "generic": {
            "format": "%(asctime)s [%(process)d] [%(levelname)s] %(message)s",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter",
        },
        "access": {
            "format": "%(asctime)s - (%(name)s)[%(levelname)s][%(host)s]: "
            + "%(request)s %(message)s %(status)d %(byte)d",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter",
        },
    },
)

logging.config.dictConfig(LOG_CONFIG)
# log = logging.getLogger("streamq.worker")
# log.info("[magenta]Hello[/]", extra={"markup": True})
try:
    queues = sys.argv[1]
except IndexError:
    queues = "default"
    
# queues = _queues.split(",")


worker = AsyncWorker(queues=queues)
worker.run()
