from time import time
from gsheet_reader import GSheetReader
from summariser import Summariser

WS_KEY = '1SJTOn0FNIzy76FH8OeSz1Ul55lJkL-ZkmWAUaa5tFGo'

def formater(num):
    return f"{num:_.2f}".replace('.', ',').replace('_', '.')

def print_records(summaries_filtered: tuple):
    actual_date_profit = [None, 0.0]

    for summ in summaries_filtered:
        d = summ['buy_date']
        if d != actual_date_profit[0]:
            if not (actual_date_profit[0] is None):
                print(f"Profit: {formater(actual_date_profit[1])}")
            
            print()
            print(str(d))
            actual_date_profit[0] = d
            actual_date_profit[1] = 0.0

        if summ['invalid'] == 1:
            print(f"{summ['ord_accum']} order(s) "\
                    "with price(s) and/or quantity(-ies) missing")
        elif summ['invalid'] == 2:
            print(f"{summ['ord_accum']} order(s) "\
                "with cost(s) and/or order number(s) missing "\
                f"(total price: {formater(summ['total_price'])})")
        else:
            tp = summ['total_price']
            c = summ['cost']
            if summ['invalid'] == 3:
                print(f"{summ['ord_accum']} order(s) "
                        "with tracking number(s) missing "\
                    f"(total price: {formater(tp)}; total cost: {formater(c)})")
            else:
                print(f"{summ['ord_accum']} valid order(s) "\
                    f"(total price: {formater(tp)}; total cost: {formater(c)})")
            actual_date_profit[1] += (tp-c)
    
    print(f"Profit: {format(actual_date_profit[1])}")

def main():
    t = time()

    gsheet_reader = GSheetReader()
    gsheet_reader.open_spreadsheet(WS_KEY)

    # 读取工作表
    print("Reading the orders...")
    t0 = time()

    # 测试时可改动range()中的数值（默认为gsheet_reader.sheets_count）
    orders_records = [gsheet_reader.get_records_from_sheet(i)
                      for i in range(100)]
    
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
