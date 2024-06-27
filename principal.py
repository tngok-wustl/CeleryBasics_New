from celery import group
from appli_celery import *
from réorg_commandes import réorg_les_comms
from globaux import NOMBRE_FEUILLES
from time import time

def formater(num):
    return f"{num:_.2f}".replace('.', ',').replace('_', '.')

if __name__ == '__main__':
    t1 = time()
    # print(appli.control.inspect().stats())
    # print(luf(245))

    # 异步读取工作表
    print("Lire les commandes...")
    t0 = time()
    r_commandes = group([luf.s(i) for i in range(1, NOMBRE_FEUILLES)]).apply_async()
    commandes = r_commandes.get()
    print(f"Durée: {time()-t0} s")
    print("Commandes lues")
    # print(commandes[20])
    # print([i for i in range(1, 300) if commandes[i-1] == 'Erreur'])
    # print("Erreurs:", commandes.count("Erreur"))

    # 排序
    print("Organiser les commandes...")
    t0 = time()
    comm_orgs = réorg_les_comms(commandes)
    print(f"Durée: {time()-t0} s")
    print("Commandes organisées")
    print(comm_orgs)

    # 按日统计订单
    print("Sommer les commandes...")
    t0 = time()
    r_sommes = group([sc.s(co, co[0][1]) for co in comm_orgs]).apply_async()
    sommes = r_sommes.get()
    print(f"Durée: {time()-t0} s")
    print("Commandes sommées")
    print(sommes)

    date_actuel = None
    for comm in sommes:
        if comm[0]['date'] != date_actuel:
            print()
            print(str(comm[0]['date']))
            date_actuel = comm[0]['date']

        if comm[0]['valide'] == False:
            print(f"{comm[1]} order(s) with cost(s) and/or order number(s) missing (total price: {formater(comm[0]['prix_total'])})")
        else:
            print(f"{comm[1]} other order(s) (total price: {formater(comm[0]['prix_total'])})")

    print(f"\nDURÉE TOTALE: {formater(time()-t1)} s")
