WS_KEY = '1SJTOn0FNIzy76FH8OeSz1Ul55lJkL-ZkmWAUaa5tFGo'

# 无效类别
class Invalids:
    VALID = 0
    NO_PRICE_QUANT = 1
    NO_COST = 2
    NO_ORD_TRACK_NR = 3

def formater(val, grouper=True, prec=2):
    if isinstance(val, int) and grouper:
        return f"{val:_}".replace('_', '.')
    elif isinstance(val, float):
        if grouper:
            return "{0:_.{1}f}".format(val, prec).replace('.', ',') \
                .replace('_', '.')
        return "{0:.{1}f}".format(val, prec).replace('.', ',')
    
    return val
