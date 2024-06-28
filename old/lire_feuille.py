import gspread
from old.globaux import *
from old.commande import Commande
# from time import sleep, time
# from gspread.exceptions import APIError
from datetime import datetime

# 将带日期的字符串转换为日期物件
def bonne_date(cdc):
    try:
        return datetime.strptime(cdc[:DATE_FIN], "%Y-%m-%dT%H:%M:%S").date()
    except ValueError:
        return None # 发现其中一张表格中有一行日期值不规范，所以忽略那一行

gc = gspread.service_account(filename="mcommandes_service.json")

doc = gc.open_by_key(GSPREAD_ID)

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
    commandes = [Commande(bonne_date(c[col_date_achat]),
                            c[col_prix],
                            c[col_quant],
                            c[col_coûte],
                            bool(c[col_no_comm]))
                            for c in flle if bonne_date(c[col_date_achat])]
    return commandes

# if __name__ == '__main__':
#     commandes = lire_une_feuille(236)
#     print(commandes)
#     print(f"Combien de commandes ici ? {len(commandes)}\n")
#     for c in commandes:
#         print(c)

# if __name__ == '__main__':
#     s = doc.worksheets()
#     print(len(s))
#     print(doc.worksheets())
#     print(s[4].get('C4'))
