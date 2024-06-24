from celery import Celery
from src.lire_feuille import lire_une_feuille
from src.sommer import sommer_comms

appli_celery = Celery('app', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

@appli_celery.task
def luf(i):
    return lire_une_feuille(i)

@appli_celery.task
def sc(tuples_comms, valide):
    return sommer_comms(tuples_comms, valide)