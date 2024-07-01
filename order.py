from datetime import date
from globals import Invalids

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
        if self['total_price'] is None:
            return Invalids.NO_PRICE_QUANT
        if self['cost'] is None:
            return Invalids.NO_COST
        if (self['ord_no'] == '') or (self['track_no'] == ''):
            return Invalids.NO_ORD_TRACK_NR
        return Invalids.VALID
    
    def __add__(self, o: dict):
        if (self['buy_date'] == o['buy_date']) and (
            self['invalid'] == o['invalid']):
            new_order = Order(ord_id='ord-id-accum', buy_date=self['buy_date'],
                              price=None, quant=None, cost=None, ord_no='',
                              track_no='',
                              ord_accum=self['ord_accum']+o['ord_accum'])
            
            if self['invalid'] != Invalids.NO_PRICE_QUANT:
                new_order['total_price'] = self['total_price'] \
                    + o['total_price']
            if self['invalid'] != Invalids.NO_COST:
                new_order['cost'] = self['cost'] + o['cost']
            if self['invalid'] != Invalids.NO_ORD_TRACK_NR:
                new_order['ord_no'] = 'ord-no-accum'
                new_order['track_no'] = 'track-no-accum'
            new_order['invalid'] = new_order.check_invalid()

            return new_order
        else:
            raise ValueError("Buy date or invalidity not match")
