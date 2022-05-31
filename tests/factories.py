
from libq import RedisJobStore, Scheduler, types


async def create_dummy_job(scheduler: Scheduler,
                           error=False,
                           qname="default") -> types.JobPayload:

    job = await scheduler.create_job(
        "examples.hello.hello_world",
        queue=qname,
        params={"timeout": 1, "error": error},
        interval="30s",
    )
    return job
