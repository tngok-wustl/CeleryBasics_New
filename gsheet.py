import gspread

gc = gspread.service_account(filename="mcommandes_service.json")

sh = gc.open("Commandes_2020 ACC 399")
print(sh.sheet1.get('B1'))