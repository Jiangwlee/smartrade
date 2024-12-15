def round_price(price: int):
    """
    将金融界的整数价格变成浮点数.
    """
    return round(price / 10000, 2)

def tag_stock(code: str, open: int, close: int, pre_close: int, high: int, low:int):
    open = round_price(open)
    close = round_price(close)
    pre_close = round_price(pre_close)
    high = round_price(high)
    low = round_price(low)
    rate = 0.1
    if code.startswith('8'):
        rate = 0.3
    elif code.startswith('3') or code.startswith('68'):
        rate = 0.2
    zt_price = round((pre_close * (1 + rate)), 2)
    dt_price = round((pre_close * (1 - rate)), 2)
    if zt_price == high and dt_price == close:
        return '天地板'
    if dt_price == low and zt_price == close:
        return '地天板'
    if zt_price == high and zt_price == low:
        return '一字板'
    if zt_price == open and zt_price == close and zt_price > low:
        return 'T字板'
    if zt_price == close:
        return '涨停'
    if dt_price == close:
        return '跌停'
    return ''

    