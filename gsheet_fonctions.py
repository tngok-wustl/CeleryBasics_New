import gspread
from gspread.exceptions import *

from dateutil import parser
from time import sleep

# 允许Google Sheet函数遇到问题重试
def gsheet_retry(func, times=3, *args, **kwargs):
    while times > 0:
        try:
            return func(*args, **kwargs)
        except (IncorrectCellLabel, InvalidInputValue,
                NoValidUrlKeyFound, SpreadsheetNotFound,
                UnSupportedExportFormat, WorksheetNotFound):
            return None
        except APIError as api_e:
            err_msg = str(api_e)
            print(err_msg)
            if 'quota exceeded' in err_msg.lower():
                sleep(60)
                times -= 1
                continue # 忽略循环中余下的代码，强制重新开始循环
        except Exception as e:
            print(str(e))
            sleep(3)
            times -= 1
    
    return None

# 生成器：从电子表（工作表物件集合）中产生订单记录，以进行数据分析
def read_sheets(worksheets):
    for ws in worksheets:
        # 第1步：忽略标题不符合日期格式规范的工作表
        title = ws.title
        try:
            _ = parser(title)
        except Exception:
            continue
        
        values = ws.get_values()
        col_names = None

        for row in ws:
            # 第2步：从每张工作表中提取列名
            if not col_names :
                if 'order-id' not in row:
                    continue 

                
                continue
        
            # 第3步：过滤掉工作表中的空行
            empty = True
            for col in ws:
                if col:
                    empty = False
                    break
            if empty:
                continue






