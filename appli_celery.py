# https://docs.celeryq.dev/en/main/userguide/tasks.html

from celery import Celery
from lire_feuille import lire_une_feuille
from sommer import sommer_comms

appli = Celery('appli_celery', broker='redis://localhost:6379/0', backend='redis://localhost:6379/1')

@appli.task(autoretry_for=(Exception,), default_retry_delay=1, max_retries=1)
def luf(i):
    return lire_une_feuille(i)

@appli.task()
def sc(tuples_comms, valide):
    return sommer_comms(tuples_comms, valide)
