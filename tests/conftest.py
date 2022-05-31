import asyncio
import os
import tempfile

import pytest
import pytest_asyncio

from libq import RedisJobStore, Scheduler, create_pool_dsn
from libq.worker import AsyncWorker

from .worker import Worker


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="module")
async def redis():
    rdb = create_pool_dsn("redis://localhost:6379")
    await rdb.flushdb()
    yield rdb
    await rdb.flushdb()


@pytest.fixture(scope="module")
async def scheduler(redis):
    store = RedisJobStore(conn=redis)
    _scheduler = Scheduler(store)
    yield _scheduler


@pytest.fixture(scope="module")
async def worker():
    rdb = create_pool_dsn("redis://localhost:6379")
    store = RedisJobStore(conn=rdb)
    _scheduler = Scheduler(store)
    worker = AsyncWorker("default", conn=rdb, scheduler=_scheduler)

    loop = asyncio.get_event_loop()
    # await loop.run_in_executor(worker.run)
    task = loop.create_task(worker.async_run())
    yield task
    task.cancel()
