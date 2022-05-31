import pytest

from libq import Queue, Scheduler, types


@pytest.mark.asyncio
async def test_job_enqueue_ok(redis, worker):
    q = Queue("default", conn=redis)
    job = await q.enqueue("examples.hello.hello_world",
                          params={"timeout": 1, "error": False},
                          timeout=55
                          )
    result = await job.get_result(timeout=3)
    assert isinstance(result, types.JobResult)
    assert result.success


@pytest.mark.asyncio
async def test_job_enqueue_bg_ok(redis, worker):
    q = Queue("default", conn=redis)
    job = await q.enqueue("examples.hello.hello_world_sync",
                          params={"timeout": 1, "error": False},
                          timeout=55,
                          background=True,
                          )
    result = await job.get_result(timeout=3)
    assert isinstance(result, types.JobResult)
    assert result.success


@pytest.mark.asyncio
async def test_job_enqueue_error(redis, worker):
    q = Queue("default", conn=redis)
    job = await q.enqueue("examples.hello.hello_world",
                          params={"timeout": 1, "error": True},
                          timeout=55,
                          max_retry=1,
                          )
    result = await job.get_result(timeout=3)
    assert isinstance(result, types.JobResult)
    assert result.success is False


@pytest.mark.asyncio
async def test_job_enqueue_bg_error(redis, worker):
    q = Queue("default", conn=redis)
    job = await q.enqueue("examples.hello.hello_world_sync",
                          params={"timeout": 1, "error": True},
                          timeout=55,
                          background=True,
                          )
    result = await job.get_result(timeout=5)
    assert isinstance(result, types.JobResult)
    assert result.success is False
