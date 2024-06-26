import gspread
from globaux import *
from commande import Commande
# from time import sleep, time
# from gspread.exceptions import APIError

gc = gspread.service_account(filename="mcommandes_service.json")

# t0 = time()
doc = gc.open("Commandes_2020 ACC 399")
# print(sh.get_worksheet(2).get('B4'))
# print(f"Durée: {time()-t0} s") # 读一格时间约为8秒

def lire_une_feuille(i):
    # t0 = time()
    print(f"{i} ici")
    # sleep(1)
    # print(f"{i} attendu")

    f = doc.get_worksheet(i).get_all_values()
    # print(f)
    # print(type(f[0][3]))
    # print(f"{len(f)} lignes, {len(f[0])} colonnes")
    # print(f"Durée: {time()-t0} s")

    # 按列名识别工作表数据
    titres = f[TITRES]
    col_date_achat = titres.index(COL_DATE_ACHAT)
    col_prix = titres.index(COL_PRIX)
    col_quant = titres.index(COL_QUANT)
    col_coûte = titres.index(COL_COÛTE)
    col_no_comm = titres.index(COL_NO_COMM)
    
    flle = f[LIGNES_ÀPD:]
    commandes = [Commande(c[col_date_achat],
                            c[col_prix],
                            c[col_quant],
                            c[col_coûte],
                            bool(c[col_no_comm]))
                            for c in flle if c[col_date_achat]]        
    return commandes

# if __name__ == '__main__':
#     commandes = lire_une_feuille(236)
#     print(commandes)
#     print(f"Combien de commandes ici ? {len(commandes)}\n")
#     for c in commandes:
#         print(c)
