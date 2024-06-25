from celery import group
from appli_celery import luf, sc
from globaux import NOMBRE_FEUILLES

def formater(num):
    return f"{num:_.2f}".replace('.', ',').replace('_', '.')

if __name__ == '__main__':
    print(luf(245))

    # print("Lire les commandes...")
    # r_commandes = group([luf.s(i) for i in range(1, NOMBRE_FEUILLES)]).apply_async()
    # commandes = r_commandes.get()
    # print("Commandes prêtes")
    # print(commandes[100])
