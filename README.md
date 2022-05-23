# Libq

This is a simple queue library based on [RQ](https://python-rq.org/) and [Arq](https://arq-docs.helpmanual.io/)

It allows to send jobs and commands to workers. 

Also, it has two main modes to perform tasks:

1. Simple [asyncio create_task](https://docs.python.org/3/library/asyncio-task.html#creating-tasks)
2. And [run_in_executor](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.run_in_executor) which choose the multiprocessing module for that. 

For an example see `run.py`


