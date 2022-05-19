import asyncio
import time


class ExampleError(Exception):
    pass


async def hello_world(timeout, error=False):
    print(f"Running hello_world, waiting {timeout}")
    await asyncio.sleep(timeout)
    if error:
        raise ExampleError

    return {"timeout": timeout, "error": error}


def hello_world_sync(timeout, error=False):
    print(f"Running hello_world, waiting {timeout}")
    time.sleep(timeout)

    if error:
        raise ExampleError

    return {"timeout": timeout, "error": error}
