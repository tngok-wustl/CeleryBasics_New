import gspread
from globals import *
import time

gc = gspread.service_account(filename="mcommandes_service.json")

# t0 = time.time()
doc = gc.open("Commandes_2020 ACC 399")
# print(sh.get_worksheet(2).get('B4'))
# print(f"Duration: {time.time()-t0} s") # 读一格时间约为8秒

def readSheet(i):
    # t0 = time.time()
    sh = doc.get_worksheet(i).get_all_values()[ROWS_START_FROM:]
    rows = len(sh)
    print(sh)
    # print(type(sh[0][3]))
    # print(f"{len(sh)} rows, {len(sh[0])} colonnes")
    # print(f"Duration: {time.time()-t0} s")

if __name__ == '__main__':
    readSheet(2)