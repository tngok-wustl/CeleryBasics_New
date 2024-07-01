from gsheet_reader import GSheetReader
from summariser import Summariser
from report_exporter import ReportExporter
from globals import WS_KEY

def main_task():
    gsheet_reader = GSheetReader()
    gsheet_reader.open_spreadsheet(WS_KEY)

    # 读取工作表
    print("Reading the orders...")
    orders_records = [gsheet_reader.get_records_from_sheet(i)
                      for i in range(gsheet_reader.sheets_count)]
    
    orders_records = list(filter(lambda n: bool(n), orders_records))
    if not orders_records:
        print(f"No orders read.")
        return
    print(f"Orders read.\n")

    summariser = Summariser(orders_records)
    summariser.group_records()

    # 累加记录
    print("Summarising up the records...")
    summaries = [summariser.sum_up(i) for i in range(summariser.grouped_count)]
    summaries = list(filter(lambda n: bool(n), summaries))
    if not summaries:
        print(f"No summaries generated.")
        return
    rec_exp = ReportExporter(summaries)
    rec_exp.summ_by_date()
    rec_exp.print_records() # 把记录印在命令提示窗中
    rec_exp.records_to_csv() # 生成csv
    print("Summaries generated. All done.")

if __name__ == '__main__':
    main_task()
