from celery import group
from appli_celery import *
from globaux import NOMBRE_FEUILLES
from time import time

def formater(num):
    return f"{num:_.2f}".replace('.', ',').replace('_', '.')

if __name__ == '__main__':
    # print(appli.control.inspect().stats())
    # print(luf(245))

    print("Lire les commandes...")

    # 异步读取工作表
    # t0 = time()
    r_commandes = group([luf.s(i) for i in range(1, NOMBRE_FEUILLES)]).apply_async()
    commandes = r_commandes.get()
    # print(f"Durée: {time()-t0} s") # 同时限制任务本身

    print("Commandes prêtes")
    # print(commandes[20])
    # print([i for i in range(1, 300) if commandes[i-1] == 'Erreur'])
    # print("Erreurs:", commandes.count("Erreur"))
