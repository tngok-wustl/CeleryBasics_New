import gspread
from gspread.exceptions import *

from dateutil import parser
from time import sleep

from order import Order

ORD_ID_KEY = 'order-id'
DATE_KEY = 'purchase-date'
PRICE_KEY = 'price'
QUANT_KEY = 'quantity-purchased'
COST_KEY = 'COST'
ORD_NO_KEY = 'ORDER NUMBER'
TRACK_NO_KEY = 'Tracking Number'

class GSheetReader():
    def __init__(self):
        self.account = gspread.service_account(
            filename="mcommandes_service.json")
        self.worksheets = None
        self.sheets_count = 0

    # 允许Google Sheet函数遇到问题重试
    def retry(self, func, tries: int, *args, **kwargs):
        for t in range(tries):
            try:
                print(f"Try {func.__name__} ({tries-t} try(-ies) left)")
                return func(*args, **kwargs)
            except (IncorrectCellLabel, InvalidInputValue,
                    NoValidUrlKeyFound, SpreadsheetNotFound,
                    UnSupportedExportFormat, WorksheetNotFound) as e:
                print(str(e))
                return None
            except APIError as api_e:
                err_msg = str(api_e)
                print(err_msg)
                if 'quota exceeded' in err_msg.lower():
                    sleep(60)
                else:
                    sleep(3)
                continue # 忽略循环中余下的代码，强制继续循环
            except Exception as e:
                print(str(e))
                sleep(3)

        print(f"No more tries for {func.__name__}")        
        return None

    # 对于不同数据，决定是否转换类型；并针对不存在的数据返回默认值
    def value_cleanup(self, indices_dict: dict, key: str,
                      line: list, action=None):
        i = indices_dict[key]
        
        if action is None: # 不转换（直接返回字串）
            if i < 0:
                return ''
            return line[i]
        else:
            if i < 0:
                return None
            try:
                return action(line[i])
            except:
                return None

    def open_spreadsheet(self, doc_key: str):
        # 第1步：打开Google电子表
        sh = self.retry(self.account.open_by_key, 1, doc_key)
        if not sh:
            print(f"ERROR: document not found. key={doc_key}")
            return

        # 第2步：获取电子表中所有工作表
        self.worksheets = self.retry(sh.worksheets, 1)
        if not self.worksheets:
            print(f"ERROR: can't get the worksheets")
        self.sheets_count = len(self.worksheets)

    def get_records_from_sheet(self, sheet_i: int):
        if sheet_i >= self.sheets_count:
            print(f"ERROR: worksheet i={sheet_i} out of range "\
                  f"for {self.sheet_count} worksheet(s)")
            return
        
        ws = self.worksheets[sheet_i]

        # 第3步：忽略空工作表、标题不符合日期格式规范的工作表
        if not ws:
            print(f"Invalid worksheet i={sheet_i}")
            return

        title = ws.title
        try:
            print(f"Parsing worksheet: '{title}'")
            _ = parser.parse(title)
        except Exception:
            print(f"Can't parse worksheet '{title}'. Ignored.")
            return
        
        values = self.retry(ws.get_values, 10)
        if not values:
            print(f"Failed to get values from worksheet '{title}'. Ignored.")
            return
        
        # 一些重要列的编号（-1表示没找到）
        ord_no_i = -1
        col_indices = {
            DATE_KEY: -1,
            PRICE_KEY: -1,
            QUANT_KEY: -1,
            COST_KEY: -1,
            ORD_NO_KEY: -1,
            TRACK_NO_KEY: -1,
        }

        records = []

        for ri, row in enumerate(values):
            # 第4步：跳过工作表中的空行
            if not any(row):
                print(f"Empty row i={ri}")
                continue

            # 第5步：从工作表中提取重要的列名
            #（订单识别码不可缺，否则该工作表所有记录无效）
            if ord_no_i < 0:
                if ORD_ID_KEY in row:
                    ord_no_i = row.index(ORD_ID_KEY)
                    for k in col_indices.keys():
                        if k in row:
                            col_indices[k] = row.index(k)

            else:
                # 第6步：整理每条记录的数据值
                ord_id = row[ord_no_i]
                if not ord_id: # 跳过缺少订单号的记录
                    print(f"Order ID missing i={ri}")
                    continue
                
                buy_date = self.value_cleanup(col_indices, DATE_KEY, row,
                                                parser.parse)
                if buy_date is None: # 跳过日期格式不规范的记录
                    print(f"Bad date i={ri}")
                    continue
                buy_date = buy_date.date()

                price = self.value_cleanup(col_indices, PRICE_KEY, row,
                                            float)
                quant = self.value_cleanup(col_indices, QUANT_KEY, row, int)
                cost = self.value_cleanup(col_indices, COST_KEY, row, float)
                ord_no = self.value_cleanup(col_indices, ORD_NO_KEY, row)
                track_no = self.value_cleanup(col_indices, TRACK_NO_KEY,
                                                row)

                # 第7步：将每条数据加入该工作表的记录单
                record = Order(ord_id, buy_date, price, quant, cost, ord_no,
                                track_no)
                records.append(record)
            
        # 第8步：返回当日的记录单
        return records

    # # 生成器：从电子表（工作表物件集合）中产生订单记录，以进行数据分析
    # def yield_sheets(self, doc_key: str):
    #     # 第1步：打开Google电子表
    #     sh = self.retry(self.account.open_by_key, 3, doc_key)
    #     if not sh:
    #         print(f"ERROR: document not found. key={doc_key}")
    #         return

    #     # 第2步：获取电子表中所有工作表
    #     worksheets = self.retry(sh.worksheets(), 3)
    #     if not worksheets:
    #         print(f"ERROR: can't get the worksheets")
    #         return

    #     for wsi, ws in enumerate(worksheets):
    #         # 第3步：忽略空工作表、标题不符合日期格式规范的工作表
    #         if not ws:
    #             print(f"Invalid worksheet i={wsi}")
    #             continue

    #         title = ws.title
    #         try:
    #             print(f"Parsing worksheet: '{title}'")
    #             _ = parser(title)
    #         except Exception:
    #             print(f"Can't parse worksheet '{title}'. Ignored.")
    #             continue
            
    #         values = self.retry(ws.get_values(), 10)
    #         if not values:
    #             print(f"Empty worksheet '{title}'. Ignored.")
    #             continue
        
    #         # 一些重要列的编号（-1表示没找到）
    #         ord_no_i = -1
    #         col_indices = {
    #             DATE_KEY: -1,
    #             PRICE_KEY: -1,
    #             QUANT_KEY: -1,
    #             COST_KEY: -1,
    #             ORD_NO_KEY: -1,
    #             TRACK_NO_KEY: -1,
    #         }

    #         records = []

    #         for ri, row in enumerate(values):
    #             # 第4步：跳过工作表中的空行
    #             if not any(row):
    #                 print(f"Empty row i={ri}")
    #                 continue

    #             # 第5步：从工作表中提取重要的列名
    #             #（订单识别码不可缺，否则该工作表所有记录无效）
    #             if ord_no_i < 0:
    #                 if ORD_ID_KEY in row:
    #                     ord_no_i = row.index(ORD_ID_KEY)
    #                     for k in col_indices.keys():
    #                         if k in row:
    #                             col_indices[k] = row.index(k)

    #             else:
    #                 # 第6步：整理每条记录的数据值
    #                 ord_id = row[ord_no_i]
    #                 if not ord_id: # 跳过缺少订单号的记录
    #                     print(f"Order ID missing i={ri}")
    #                     continue
                    
    #                 buy_date = self.value_cleanup(col_indices, DATE_KEY, row,
    #                                               parser)
    #                 if buy_date is None: # 跳过日期格式不规范的记录
    #                     print(f"Bad date i={ri}")
    #                     continue

    #                 price = self.value_cleanup(col_indices, PRICE_KEY, row,
    #                                            float)
    #                 quant = self.value_cleanup(col_indices, QUANT_KEY, row, int)
    #                 cost = self.value_cleanup(col_indices, COST_KEY, row, float)
    #                 ord_no = self.value_cleanup(col_indices, ORD_NO_KEY, row)
    #                 track_no = self.value_cleanup(col_indices, TRACK_NO_KEY,
    #                                               row)

    #                 # 第7步：将每条数据加入该工作表的记录单
    #                 record = Order(ord_id, buy_date, price, quant, cost, ord_no,
    #                                track_no)
    #                 records.append(record)
                
    #         # 第8步：生成当日的记录单
    #         yield(records)
