import time

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

sched = BlockingScheduler()


def job_function():
    print(time.time(), "job_function")


class TestObj(object):
    def __init__(self, test1):
        print(test1)

    def start(self):
        pass


if __name__ == '__main__':
    sched.add_job(job_function, CronTrigger.from_crontab('*/1 * * * *'))
    # sched.add_job(TestObj("test").start, CronTrigger.from_crontab('*/1 * * * *'))
    sched.start()
