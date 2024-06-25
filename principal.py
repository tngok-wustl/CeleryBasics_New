from celery import group
from appli_celery import luf, sc
from globaux import NOMBRE_FEUILLES

def formater(num):
    return f"{num:_.2f}".replace('.', ',').replace('_', '.')

if __name__ == '__main__':
    print("Lire les commandes...")
    commandes = group([luf.s(i) for i in range(1, NOMBRE_FEUILLES)])().get()
    print("Commandes prêtes")
    print(commandes[100])
