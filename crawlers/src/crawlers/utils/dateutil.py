import time
from datetime import date, datetime

def today():
    return date.today().strftime("%Y%m%d")
        
def timestampInMilliseconds():
    return int(time.time() * 1000)