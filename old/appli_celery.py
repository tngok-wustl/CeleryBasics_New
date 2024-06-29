# https://docs.celeryq.dev/en/main/userguide/tasks.html

from celery import Celery
from old.lire_feuille import lire_une_feuille
from old.sommer import sommer_comms
from gspread.exceptions import APIError
from celery.exceptions import MaxRetriesExceededError

appli = Celery('appli_celery', broker='redis://localhost:6379/0', backend='redis://localhost:6379/1')

# @appli.task(
        # bind=True,
        # autoretry_for=(Exception,),
        # default_retry_delay=0,
        # retry_backoff=True,
        # max_retries=3,
        # )
@appli.task(rate_limit='1/s')
def luf(self, i):
    try:
        try:
            return lire_une_feuille(i)
        except APIError as api_e:
            print(api_e)
            raise self.retry(countdown=60)
        except BaseException as e:
            print(f"Err: {type(e)}")
            print(e)
            raise self.retry(countdown=1, max_retries=10)
    except MaxRetriesExceededError:
        return "Erreur"

@appli.task()
def sc(tuples_comms, valide):
    return sommer_comms(tuples_comms, valide)
