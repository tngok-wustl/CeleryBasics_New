from time import time
from gsheet_reader import GSheetReader
from summariser import Summariser
from report_exporter import ReportExporter
from globals import *

def main():
    t = time()

    gsheet_reader = GSheetReader()
    gsheet_reader.open_spreadsheet(WS_KEY)

    # 读取工作表
    print("Reading the orders...")
    t0 = time()

    # 测试时可改动range()中的数值（默认为gsheet_reader.sheets_count）
    orders_records = [gsheet_reader.get_records_from_sheet(i)
                      for i in range(gsheet_reader.sheets_count)]
    
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

    rec_exp = ReportExporter(summaries)
    rec_exp.print_records()
    print()
    print(f"All done. Duration: {formater(time()-t)} s")

if __name__ == '__main__':
    main()
