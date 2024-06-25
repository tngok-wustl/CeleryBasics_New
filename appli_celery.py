from celery import Celery
from lire_feuille import lire_une_feuille
from sommer import sommer_comms

appli = Celery('appli_celery', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

@appli.task()
def luf(i):
    return lire_une_feuille(i)

@appli.task()
def sc(tuples_comms, valide):
    return sommer_comms(tuples_comms, valide)
