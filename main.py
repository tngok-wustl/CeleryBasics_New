from time import time
from gsheet_reader import GSheetReader
from summariser import Summariser

WS_KEY = '1SJTOn0FNIzy76FH8OeSz1Ul55lJkL-ZkmWAUaa5tFGo'

def formater(num):
    return f"{num:_.2f}".replace('.', ',').replace('_', '.')

def print_records(summaries_filtered: tuple):
    actual_date = None

    for summ in summaries_filtered:
        d = summ['buy_date']
        if d != actual_date:
            print()
            print(str(d))
            actual_date = d

        if summ['invalid'] == 1:
            print(f"{summ['ord_accum']} order(s) "\
                    "with price(s) and/or quantity(-ies) missing")
        elif summ['invalid'] == 2:
            print(f"{summ['ord_accum']} order(s) "\
                "with cost(s) and/or order number(s) missing "\
                f"(total price: {formater(summ['total_price'])})")
        elif summ['invalid'] == 3:
            print(f"{summ['ord_accum']} order(s) "
                    "with tracking number(s) missing "\
                f"(total price: {formater(summ['total_price'])}; "\
                f"total cost: {formater(summ['cost'])})")
        else:
            print(f"{summ['ord_accum']} valid order(s) "\
                f"(total price: {formater(summ['total_price'])}; "\
                f"total cost: {formater(summ['cost'])})")
def main():
    t = time()

    gsheet_reader = GSheetReader()
    gsheet_reader.open_spreadsheet(WS_KEY)

    # 读取工作表
    print("Reading the orders...")
    t0 = time()
    orders_records = [gsheet_reader.get_records_from_sheet(i)
                      for i in range(30)] # 测试时可改动range()中的数字
    orders_records = list(filter(lambda n: bool(n), orders_records))
    if not orders_records:
        print(f"No orders read. Duration: {formater(time()-t0)} s")
        return
    print(f"Orders read. Duration: {formater(time()-t0)} s\n")

    summariser = Summariser(orders_records)
    summariser.group_records()
    # print(summariser.grouped_records)

    # 累加记录
    print("Summarising up the records...")
    t0 = time()
    summaries = [summariser.sum_up(i) for i in range(summariser.grouped_count)]
    summaries = list(filter(lambda n: bool(n), summaries))
    if not summaries:
        print(f"No summaries generated. Duration: {formater(time()-t0)} s")
        return
    print(f"Summaries generated. Duration: {formater(time()-t0)} s")

    print_records(summaries)
    print()
    print(f"All done. Duration: {formater(time()-t)} s")

if __name__ == '__main__':
    main()
