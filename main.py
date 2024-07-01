from time import time
from gsheet_reader import GSheetReader
from summariser import Summariser
from report_exporter import ReportExporter
from globals import WS_KEY, formater

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
    # orders_records = [gsheet_reader.get_records_from_sheet(i)
    #                   for i in range(10)]
    
    orders_records = list(filter(lambda n: bool(n), orders_records))
    if not orders_records:
        print(f"No orders read. Duration: {formater(time()-t0, prec=6)} s")
        return
    print(f"Orders read. Duration: {formater(time()-t0, prec=6)} s\n")

    summariser = Summariser(orders_records)
    summariser.group_records()
    # print(summariser.grouped_records)

    # 累加记录
    print("Summarising up the records...")
    t0 = time()
    summaries = [summariser.sum_up(i) for i in range(summariser.grouped_count)]
    summaries = list(filter(lambda n: bool(n), summaries))
    if not summaries:
        print(f"No summaries generated. " \
              f"Duration: {formater(time()-t0, prec=6)} s\n")
        return
    print(f"Summaries generated. Duration: {formater(time()-t0, prec=6)} s\n")

    rec_exp = ReportExporter(summaries)
    rec_exp.summ_by_date()
    rec_exp.print_records() # 把记录印在命令提示窗中

    # 生成csv
    t0 = time()
    rec_exp.records_to_csv()
    print("Summaries exported to CSV. " \
          f"Duration: {formater(time()-t0, prec=6)} s\n")
    
    print(f"All done. Duration: {formater(time()-t, prec=6)} s")

if __name__ == '__main__':
    main()
