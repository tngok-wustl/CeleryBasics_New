from datetime import datetime
from globaux import DATE_FIN
# from datetime import date

# 必须创建基于dict的数据类型，否则无法使用celery
class Commande(dict):
    def __init__(self, date, prix=0.0, quant=1, coûte='', no_comm=False):
        la_date = self.dater(date) if isinstance(date, str) else date # 这样就不用在外面转换字符串了

        le_prix = float(prix) if isinstance(date, str) else prix
        la_quant = int(quant) if isinstance(date, str) else quant

        super().__init__(date=la_date,
                         prix_total=le_prix*la_quant,
                         coûte=coûte,
                         no_comm=no_comm)
        self['valide'] = self.valider()

    # 将带日期的字符串转换为日期物件
    def dater(self, date_brute):
        try:
            return datetime.strptime(date_brute[:DATE_FIN], "%Y-%m-%dT%H:%M:%S").date()
        except ValueError:
            return "" # 发现其中一张表格中有一行日期值不规范，所以忽略那一行

    def valider(self):
        if (self['coûte'] == '') or (not self['no_comm']):
            return False
        
        if isinstance(self['coûte'], str):
            self['coûte'] = float(self['coûte'])
        return True
    
    def __add__(self, c):
        nouv_pt = self['prix_total'] + c['prix_total']
        nouv_coûte = self['coûte'] + c['coûte']
        return Commande(self['date'], nouv_pt, 1, nouv_coûte, self['no_comm'])

# if __name__ == '__main__':
#     c1 = Commande("2020-12-10T00:41:15", 59.52)
#     c2 = Commande("2020-12-10T22:34:50", 49.27)
#     c3 = Commande("2020-12-10T07:29:06", 122.79)

#     C = sum([c1, c2, c3], start=Commande(date(2020, 12, 10)))
#     print(C)
