import gspread
from globaux import *
from commande import Commande
# import time

gc = gspread.service_account(filename="mcommandes_service.json")

# t0 = time.time()
doc = gc.open("Commandes_2020 ACC 399")
# print(sh.get_worksheet(2).get('B4'))
# print(f"Durée: {time.time()-t0} s") # 读一格时间约为8秒

def lire_une_feuille(i):
    # t0 = time.time()
    flle = doc.get_worksheet(i).get_all_values()[LIGNES_ÀPD:]
    # print(f"Durée: {time.time()-t0} s")

    # print(sh)
    # print(type(sh[0][3]))
    # print(f"{len(sh)} lignes, {len(sh[0])} colonnes")

    commandes = [Commande(c[COL_DATE_ACHAT],
                              c[COL_PRIX],
                              c[COL_QUANT],
                              c[COL_COÛTE],
                              c[COL_NO_COMM])
                              for c in flle]        
    return commandes

# if __name__ == '__main__':
#     commandes = lire_une_feuille(2)
#     print(f"Combien de commandes ici ? {len(commandes)}\n")
#     for c in commandes:
#         print(c)