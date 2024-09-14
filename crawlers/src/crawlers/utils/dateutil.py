import time
import requests
from typing import List
from datetime import date, datetime, timedelta
from crawlers.utils.logger import getLogger
from crawlers.jrj.dto import StockHangQingInfo

log = getLogger()

def today():
    return date.today().strftime("%Y%m%d")
        
def timestampInMilliseconds():
    return int(time.time() * 1000)

def timestampToDatetime(timestamp: str) -> datetime:
    return datetime.fromtimestamp(int(timestamp))

def previousDate(date_str: str):
    date_format = "%Y%m%d"
    # 将字符串转换为日期对象
    target_date = datetime.strptime(date_str, date_format)
    # 获取前一天的日期
    previous_day = target_date - timedelta(days=1)
    # 格式化前一天的日期
    return previous_day.strftime(date_format)

def nextDate(date_str: str):
    date_format = "%Y%m%d"
    # 将字符串转换为日期对象
    target_date = datetime.strptime(date_str, date_format)
    # 获取下一天的日期
    next_day = target_date + timedelta(days=1)
    # 格式化一天的日期
    return next_day.strftime(date_format)

def offsetInMinutes(cur_time: datetime, start_time: str = "09:25") -> int:
    formatted_time = cur_time.strftime("%H:%M")
    cur_date = datetime.today().strftime("%Y-%m-%d")
    # 将时分字符串与日期结合，并转换为datetime对象
    start_obj = datetime.strptime(cur_date + " " + start_time, "%Y-%m-%d %H:%M")
    now_obj = datetime.strptime(cur_date + " " + formatted_time, "%Y-%m-%d %H:%M")
    # 计算两个时间之间的差异
    time_diff = now_obj - start_obj
    # 将时间差转换为分钟
    return time_diff.total_seconds() / 60

"""
获取过去的 N 个交易日.
"""
def getLastNTradeDate(num: int) -> List[str]:
    url = f"https://gateway.jrj.com/quot-kline?format=json&securityId=1000001&type=day&direction=left&range.num={num}"
    result = []
    response = requests.get(url)
    if response.status_code == 200:
        content = response.json()
        log.info("查询交易日信息成功!")
        data = [StockHangQingInfo(code="000001", **item) for item in content["data"]["kline"]]
        result = [d.index for d in data]
        return result
    else:
        log.error(f"请求失败，状态码: {response.status_code}")


"""
A date iterator between start and end.
"""
class DateIterator:
    def __init__(self, start: str, end: str, format: str = "%Y%m%d") -> None:
        self.format = format
        self.start = datetime.strptime(start, format)
        self.end = datetime.strptime(end, format)
        self.date = self.start

    def next(self):
        if self.hasNext():
            self.date = self.date + timedelta(days=1)
        return self.date.strftime(self.format)
    
    def prev(self):
        if self.hasPrev():
            self.date = self.date - timedelta(days=1)
        return self.date.strftime(self.format)
    
    def hasNext(self):
        return self.date < self.end;

    def hasPrev(self):
        return self.date > self.start;

if __name__ == '__main__':
    for t in [1726191000, 1722821460, 1722821520, 1726124340]:
        print(timestampToDatetime(t))