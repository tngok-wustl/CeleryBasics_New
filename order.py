from datetime import date

class Order(dict):
    def __init__(self, ord_id: str, buy_date: date, price: float = None,
                 quant: int = None, cost: float = None, ord_no: str = '',
                 track_no: str = '', ord_accum: int = 1):
        super().__init__(ord_id=ord_id, buy_date=buy_date,
                         total_price=None, cost=cost,
                         ord_no=ord_no, track_no=track_no, ord_accum=ord_accum)
        if (not (price is None)) and (not (quant is None)):
            self['total_price'] = price * float(quant)
        self['invalid'] = self.check_invalid()
    
    # 无效订单分类（0类为有效订单）
    def check_invalid(self):
        if (self['price'] is None) or (self['quant'] is None):
            return 1
        if (self['cost'] is None) or (self['ord_no'] == ''):
            return 2
        if self['track_no'] == '':
            return 3
        return 0
    
    def __add__(self, o: dict):
        if (self['buy_date'] == o['buy_date']) and (
            self['invalid'] == o['invalid']):
            new_order = Order(ord_id='ord-id-accum', buy_date=self['buy_date'],
                              price=None, quant=None, cost=None, ord_no='',
                              track_no='',
                              ord_accum=self['ord_accum']+o['ord_accum'])
            
            if self['invalid'] != 1:
                new_order['total_price'] = self['total_price']
                + o['total_price']
            if self['invalid'] != 2:
                new_order['cost'] = self['cost'] + o['cost']
                new_order['ord_no'] = 'ord-no-accum'
            if self['invalid'] != 3:
                new_order['track_no'] = 'track-no-accum'

            return new_order
        else:
            raise ValueError("Buy date or invalidity not match")
