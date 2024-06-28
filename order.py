from datetime import date

class Order(dict):
    def __init__(self, ord_id: str, buy_date: date, price: float = None,
                 quant: int = None, cost: float =None, ord_no: str = '',
                 track_no: str =''):
        super().__init__(ord_id=ord_id, buy_date=buy_date,
                         total_price=price*float(quant), cost=cost,
                         ord_no=ord_no, track_no=track_no)
        self['invalid'] = self.check_invalid()
    
    # 无效订单分类（0类为有效订单）
    def check_invalid(self):
        if (self['price'] is None) or (self['quant'] is None):
            return 1
        if (self['cost'] is None) or (not self['ord_no']):
            return 2
        if (not self['track_no']):
            return 3
        return 0
    
    