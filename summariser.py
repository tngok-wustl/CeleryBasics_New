from gsheet_reader import GSheetReader
from order import Order

from itertools import chain, groupby
from operator import itemgetter

class Summariser():
    def __init__(self, records_list):
        # 将所有订单物件放在一个大清单中
        self.records = list(chain.from_iterable(records_list))

        # 然后按购买日期及无效类别排序并重组订单
        self.records.sort(key=itemgetter('buy_date', 'invalid'))

    def sum_up(self):
        for key, rec in self.records:
            buy_date = key[0]
            invalid = key[1]

            start_item = Order(ord_id='ord-id-start', buy_date=buy_date,
                               price=None, quant=None, cost=None, ord_no='',
                               track_no='', ord_accum=0)
            if invalid != 1:
                start_item['total_price'] = 0.0
            if self['invalid'] != 2:
                start_item['cost'] = 0.0
                start_item['ord_no'] = 'ord-no-start'
            if self['invalid'] != 3:
                start_item['track_no'] = 'track-no-start'

            yield sum(rec, start=start_item)
