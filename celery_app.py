# https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html

from celery import Celery
from celery.schedules import crontab
from main_task import main_task

app = Celery('task', broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/1')

@app.on_after_configure.connect
def auto_schedule(sender: Celery, **kwargs):
    sender.add_periodic_task(
        crontab(minute='*/15', hour='*'),
        summ_profit.s(),
    )

@app.task
def summ_profit():
    main_task()
