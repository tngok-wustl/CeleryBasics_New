from order import Order
from globals import Invalids
from itertools import chain, groupby
from operator import itemgetter

class Summariser():
    def __init__(self, records_list):
        # 将所有订单物件放在一个大清单中
        self.records = []
        self.grouped_records = []
        self.grouped_count = 0

        if records_list:
            self.records = list(chain.from_iterable(records_list))

    # 然后按购买日期及无效类别排序并重组订单
    def group_records(self):
        if not self.records:
            print(f"ERROR: No records to group.")
            return
        
        self.records.sort(key=itemgetter('buy_date', 'invalid'))
        self.grouped_records = [(cl, list(gr)) for cl, gr in
                                groupby(self.records,
                                        key=itemgetter('buy_date', 'invalid'))]
        self.grouped_count = len(self.grouped_records)

    # 累加重组之后的订单
    def sum_up(self, group_i: int):
        if group_i > self.grouped_count:
            print(f"ERROR: record i={group_i} out of range "\
                  f"for {self.grouped_count} record(s)")
            return
        
        grouped_record = self.grouped_records[group_i]
        buy_date = grouped_record[0][0]
        invalid = grouped_record[0][1]
        rec = grouped_record[1]

        start_item = Order(ord_id='ord-id-start', buy_date=buy_date,
                            price=None, quant=None, cost=None, ord_no='',
                            track_no='', ord_accum=0)
        if invalid != Invalids.NO_PRICE_QUANT:
            start_item['total_price'] = 0.0
        if invalid != Invalids.NO_COST:
            start_item['cost'] = 0.0
        if invalid != Invalids.NO_ORD_TRACK_NR:
            start_item['ord_no'] = 'ord-no-start'
            start_item['track_no'] = 'track-no-start'
        start_item['invalid'] = start_item.check_invalid()

        return sum(rec, start=start_item)
