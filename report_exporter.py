from globals import formater

class ReportExporter():
    def __init__(self, summaries: tuple):
        self.summaries = summaries

    def print_records(self):
        actual_date_profit = [None, 0.0]

        for summ in self.summaries:
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
        
        print(f"Profit: {formater(actual_date_profit[1])}")

    def records_to_csv(self):
        pass
