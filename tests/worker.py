from multiprocessing import Process

from libq import RedisJobStore, Scheduler
from libq.worker import AsyncWorker

# from threading import Thread



class Worker(Process):

    def __init__(self, redis, queues="default", scheduler=False):
        Process.__init__(self)
        self.store = RedisJobStore(conn=redis)
        if scheduler:
            _scheduler = Scheduler(self.store)
            self.worker = AsyncWorker(queues=queues, scheduler=_scheduler)
        else:
            self.worker = AsyncWorker(queues=queues)

    def run(self):
        self.worker.run()
