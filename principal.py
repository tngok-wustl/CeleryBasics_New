from celery import group
from appli_celery import luf, sc
from globaux import NOMBRE_FEUILLES
from time import time

def formater(num):
    return f"{num:_.2f}".replace('.', ',').replace('_', '.')

if __name__ == '__main__':
    # print(luf(245))

    print("Lire les commandes...")

    # 异步读取工作表
    t0 = time()

    # 待解决（奇怪问题）：超过Google API使用限制的错误？
    r_commandes = group([luf.s(i) for i in range(1, NOMBRE_FEUILLES)]).apply_async()
    commandes = r_commandes.get()

    print(f"Durée: {time()-t0} s")

    print("Commandes prêtes")
    print(commandes[20])
