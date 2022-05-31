import logging
import sys
from logging import config
from typing import Any, Dict

from rich.logging import RichHandler

from libq import RedisJobStore, Scheduler, types
from libq.worker import AsyncWorker

# from libq.job_store import RedisJobStore

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


async def create_dummy_job(scheduler: Scheduler, qname="default") -> types.JobPayload:

    job = await scheduler.create_job(
        "examples.hello.hello_world",
        queue=qname,
        params={"timeout": 1, "error": False},
        interval="30s",
    )
    return job


if __name__ == "__main__":
    logging.config.dictConfig(LOG_CONFIG)
    # log = logging.getLogger("streamq.worker")
    # log.info("[magenta]Hello[/]", extra={"markup": True})
    try:
        queues = sys.argv[1]
    except IndexError:
        queues = "default"
    # queues = _queues.split(",")

    store = RedisJobStore()
    scheduler = Scheduler(store)

    worker = AsyncWorker(queues=queues, scheduler=scheduler)
    worker.run()
