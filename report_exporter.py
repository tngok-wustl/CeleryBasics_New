from globals import formater, Invalids
import csv

class ReportExporter():
    def __init__(self, summaries):
        self.summaries = []
        self.summ_dicts = []

        if summaries:
            self.summaries = summaries

    def summ_by_date(self):
        if not self.summaries:
            print("ERROR: Nothing to summarise.")
            return
        
        summ_dict = {
            'purchase-date': None,
            }
        for summ in self.summaries:
            if summ['buy_date'] != summ_dict['purchase-date']:
                if not (summ_dict['purchase-date'] is None):
                    self.summ_dicts.append(summ_dict)
                    
                summ_dict = {
                    'purchase-date': summ['buy_date'],
                    'valid-count': 0,
                    'valid-price': 0.0,
                    'valid-cost': 0.0,
                    'no-price-quant-count': 0,
                    'no-cost-count': 0,
                    'no-cost-price': 0.0,
                    'no-ord-track-nr-count': 0,
                    'no-ord-track-nr-price': 0.0,
                    'no-ord-track-nr-cost': 0.0,
                    'profit': 0.0,
                    }
            
            if summ['invalid'] == Invalids.NO_PRICE_QUANT:
                summ_dict['no-price-quant-count'] = summ['ord_accum']
            elif summ['invalid'] == Invalids.NO_COST:
                summ_dict['no-cost-count'] = summ['ord_accum']
                summ_dict['no-cost-price'] = summ['total_price']
            else:
                if summ['invalid'] == Invalids.NO_ORD_TRACK_NR:
                    summ_dict['no-ord-track-nr-count'] = summ['ord_accum']
                    summ_dict['no-ord-track-nr-price'] = summ['total_price']
                    summ_dict['no-ord-track-nr-cost'] = summ['cost']
                else:
                    summ_dict['valid-count'] = summ['ord_accum']
                    summ_dict['valid-price'] = summ['total_price']
                    summ_dict['valid-cost'] = summ['cost']
                summ_dict['profit'] += summ['total_price']
                summ_dict['profit'] -= summ['cost']
        self.summ_dicts.append(summ_dict)

    def print_records(self):
        if not self.summ_dicts:
            print("ERROR: No summaries to print.")
            return

        for sd in self.summ_dicts:
            print(str(sd['purchase-date']))
            print(f"{formater(sd['valid-count'])} valid order(s) " \
                  f"(total price: {formater(sd['valid-price'])}; " \
                    f"total cost: {formater(sd['valid-cost'])})")
            print(f"{formater(sd['no-price-quant-count'])} order(s) " \
                  "with price(s) and/or quantity(s) missing")
            print(f"{formater(sd['no-cost-count'])} order(s) " \
                  "with cost(s) missing " \
                    f"(total price: {formater(sd['no-cost-price'])})")
            print(f"{formater(sd['no-ord-track-nr-count'])} order(s) " \
                  "with order number(s) and/or tracking number(s) missing " \
                  f"(total price: {formater(sd['no-ord-track-nr-price'])}; " \
                    f"total cost: {formater(sd['no-ord-track-nr-cost'])})")
            print(f"Profit: {formater(sd['profit'])}")
            print()

    def records_to_csv(self):
        if not self.summ_dicts:
            print("ERROR: No summaries to export.")
            return
        
        with open('records.csv', 'w', newline='') as f:
            fieldnames = self.summ_dicts[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';',
                                    quoting=csv.QUOTE_NONNUMERIC)
            writer.writeheader()
            for r in self.summ_dicts:
                r_form = {k: formater(v, False) for k, v in r.items()}
                writer.writerow(r_form)
        f.close()
