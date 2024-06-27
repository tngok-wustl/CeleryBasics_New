import datetime
import re
import time
import traceback
import logging
import sys

import dateutil
import dateutil.parser
import gspread
from gspread import WorksheetNotFound, CellNotFound
from gspread.exceptions import (
  APIError, CellNotFound, GSpreadException, IncorrectCellLabel, InvalidInputValue,
  NoValidUrlKeyFound, SpreadsheetNotFound, UnSupportedExportFormat, WorksheetNotFound)
from google.oauth2 import service_account

logger = logging.getLogger()
formatter = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s')
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


class SheetAPI(object):
  scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
  ]

  def __init__(self, service_account_data):
    credentials = service_account.Credentials.from_service_account_info(
      service_account_data, scopes=self.scopes)
    self.service = gspread.authorize(credentials)

  def get_spreadsheet(self, spreadsheet_id):
    return self.retry(self.service.open_by_key, spreadsheet_id)

  def get_worksheets(self, spreadsheet):
    return self.retry(spreadsheet.worksheets)

  def get_worksheet_vals(self, worksheet):
    return self.retry(worksheet.get_all_values)

  def find_or_create_sheet(self, spreadsheet, sheet_name, template_name='template'):
    worksheet = None
    try:
      worksheet = self.retry(spreadsheet.worksheet, sheet_name)
    except WorksheetNotFound:
      try:
        template_worksheet = self.retry(spreadsheet.worksheet, template_name)
        worksheet = template_worksheet.duplicate(new_sheet_name=sheet_name)
      except WorksheetNotFound as e:
        raise Exception('Template sheet %s not found' % template_name)

    return worksheet

  def append_row_by_key(self, worksheet, key, data=None):
    if data is None:
      data = {}

    cell = self.retry(worksheet.find, key)
    if cell:
      return

    row_data = list(data.values())
    self.retry(worksheet.append_row, row_data, table_range='A1:BB1', value_input_option='RAW')

  def find_cell_by_key(self, worksheet, key):
    return self.retry(worksheet.find, key)

  def update_worksheet_cell(self, worksheet, row, col, value):
    self.retry(worksheet.update_cell, row, col, value)

  def delete_rows(self, worksheet, start_index, end_index=None):
    return self.retry(worksheet.delete_rows, start_index, end_index)

  def create_new_sheet_if_not_existed(self, spreadsheet_id, sheet_name, template_name='template'):
    # check if existed
    gc = self.service.open_by_key(spreadsheet_id)
    try:
      worksheet = gc.worksheet(sheet_name)
      print('sheet %s already existed' % sheet_name)
      return worksheet
    except APIError as e:
      message = str(e)
      print(message)
      time.sleep(30)
      return self.create_new_sheet_if_not_existed(spreadsheet_id, sheet_name, template_name=template_name)
    except WorksheetNotFound as e:
      logger.error('sheet %s not existed, will try to create' % sheet_name)

    try:
      template_worksheet = gc.worksheet(template_name)
    except WorksheetNotFound as e:
      raise Exception('Template sheet %s not found' % template_name)

    return template_worksheet.duplicate(new_sheet_name=sheet_name)

  def retry(self, method, *args, **kwargs):
    result = None
    max_retries = 7
    while max_retries > 0:
      try:
        result = method(*args, **kwargs)
        break
      except (CellNotFound, IncorrectCellLabel, InvalidInputValue, NoValidUrlKeyFound, SpreadsheetNotFound, UnSupportedExportFormat, WorksheetNotFound):
        raise
      except gspread.exceptions.APIError as e:
        quota_error = False
        try:
          resp = e.response.json()
          logger.warning(resp)
          if resp['code'] == 429:
            quota_error = True
        except:
          message = str(e)
          logger.warning(message)
          if "quota exceeded" in message.lower():
            quota_error = True

        if quota_error:
          time.sleep(60)

          max_retries -= 1
          continue
      except Exception as e:
        logger.exception(e)
        time.sleep(3)

        max_retries -= 1

    return result


class OrderReader(object):
  pass


class GSheetOrderReader(OrderReader):
  def __init__(self, sheet_api):
    self.sheet_api = sheet_api

  def read(self, spreadsheet_id, days=7, include_today=True):
    today = datetime.datetime.utcnow()
    if include_today:
      to_date = today
    else:
      to_date = today - datetime.timedelta(days=1)
    from_date = today - datetime.timedelta(days=days)

    logger.debug('[SheetProcessing] %s', spreadsheet_id)

    spreadsheet = self.sheet_api.get_spreadsheet(spreadsheet_id)
    if not spreadsheet:
      logger.error('[SpreadSheetNotFound] %s', spreadsheet_id)
      return

    worksheets = self.sheet_api.get_worksheets(spreadsheet)
    for worksheet in worksheets:
      records = []
      name = worksheet.title
      try:
        sheet_date = dateutil.parser.parse(name)

        if not sheet_date or sheet_date < from_date or sheet_date > to_date:
          # logger.debug('[SheetIgnored] %s', name)
          continue
      except Exception as e:
        # None date sheets
        continue

      logger.debug('[Sheet] SheetID: %s, SheetName: %s', spreadsheet_id, name)

      vals = self.sheet_api.get_worksheet_vals(worksheet)
      headers = None
      for row in vals:
        if not headers:
          if 'tracking' not in row and 'Tracking' not in row and 'Tracking Number' not in row:
            continue

          headers = [col.lower() for col in row]
          continue

        empty = True
        for col in row:
          if col:
            empty = False
            break

        if empty:
          continue

        record = {'spreadsheet_id': spreadsheet_id, 'sheet': name}
        for idx, header in enumerate(headers):
          try:
            record[header] = row[idx]
          except Exception as e:
            logger.exception(e)

        order_number = None
        item_sku = None
        if 'sku' in record and record['sku']:
          if record['sku'].startswith('EM'):
            order_number = '-'.join(record['sku'].split('-')[:2])
            item_sku = record['sku'].replace('{}-'.format(order_number), '')
        elif 'sales channel' in record and record['sales channel']:
          order_number = '-'.join(record['sales channel'].split('-')[0:2])
        elif 'em order number' in record and record['em order number']:
          order_number = record['em order number']
        else:
          logger.info('[OrderNumberNotFound] %s', record)
          continue

        if not order_number:
          continue

        record['order_number'] = order_number
        record['item_sku'] = item_sku if item_sku else record.get('sku', '')
        records.append(record)

      yield (worksheet, headers, records)
