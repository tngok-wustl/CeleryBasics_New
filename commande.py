from datetime import datetime

class Commande():
    def __init__(self, date, prix_total=0.0, coUte='', no_comm=False):
        # 这样就不用在外面转换字符串了
        self.date = self.dater(date) if isinstance(date, str) else date
        self.prix_total = float(prix_total) if isinstance(date, str) else prix_total
        self.coUte = coUte
        
        self.no_comm = no_comm # 订单号是否存在
        
        self.valide = self.valider()

    # 将带日期的字符串转换为日期
    def dater(self, date_brute):
        return datetime.strptime(date_brute, "%Y-%m-%dT%H:%M:%S").date()

    def valider(self):
        if (self.coUte == '') or (not self.no_comm):
            return False
        
        if isinstance(self.coUte, str):
            self.coUte = float(self.coUte)
        return True
    
    def __add__(self, c):
        nouv_pt = self.prix_total + c.prix_total
        nouv_coUte = self.coUte + c.coUte
        return Commande(self.date, nouv_pt, nouv_coUte, self.no_comm)

# if __name__ == '__main__':
#     c1 = Commande("2020-12-10T00:41:15", 59.52)
#     c2 = Commande("2020-12-10T22:34:50", 49.27)
#     c3 = Commande("2020-12-10T07:29:06", 122.79)

#     C = sum([c1, c2, c3], start=Commande("2020-12-10T00:00:00"))
#     print(C.date, C.prix_total, C.coUte, C.no_comm, C.valide)