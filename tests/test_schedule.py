import pytest

from libq import Queue, Scheduler, types

from .factories import create_dummy_job


@pytest.mark.asyncio
async def test_scheduler_obj(scheduler):
    assert isinstance(scheduler, Scheduler)


async def test_scheduler_job(scheduler: Scheduler):
    job = await create_dummy_job(scheduler)
    await scheduler.enqueue_job(job.jobid)
    enqueued = await scheduler.get_enqueued()
    _job = await scheduler.store.get(job.jobid)
    assert len(enqueued) > 0
    assert _job.jobid == job.jobid
