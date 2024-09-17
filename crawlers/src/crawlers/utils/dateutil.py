import time
import requests
from typing import List
from datetime import date, datetime, timedelta
from crawlers.utils.logger import get_logger
from crawlers.jrj.dto import StockHangQingInfo

log = get_logger()

def today():
    return date.today().strftime("%Y%m%d")
        
def timestamp_in_milliseconds():
    return int(time.time() * 1000)

def timestamp_to_datetime(timestamp: str) -> datetime:
    return datetime.fromtimestamp(int(timestamp))

def previous_date(date_str: str):
    date_format = "%Y%m%d"
    # 将字符串转换为日期对象
    target_date = datetime.strptime(date_str, date_format)
    # 获取前一天的日期
    previous_day = target_date - timedelta(days=1)
    # 格式化前一天的日期
    return previous_day.strftime(date_format)

def next_date(date_str: str):
    date_format = "%Y%m%d"
    # 将字符串转换为日期对象
    target_date = datetime.strptime(date_str, date_format)
    # 获取下一天的日期
    next_day = target_date + timedelta(days=1)
    # 格式化一天的日期
    return next_day.strftime(date_format)

def offset_in_minutes(cur_time: datetime, start_time: str = "09:25") -> int:
    formatted_time = cur_time.strftime("%H:%M")
    cur_date = datetime.today().strftime("%Y-%m-%d")
    # 将时分字符串与日期结合，并转换为datetime对象
    start_obj = datetime.strptime(cur_date + " " + start_time, "%Y-%m-%d %H:%M")
    now_obj = datetime.strptime(cur_date + " " + formatted_time, "%Y-%m-%d %H:%M")
    # 计算两个时间之间的差异
    time_diff = now_obj - start_obj
    # 将时间差转换为分钟
    return time_diff.total_seconds() / 60

def compare_date(date1: str, date2: str):
    """
    比较两个日期.
    --
    @param data1: 第一个日期, 格式: %Y%m%d
    @param data2: 第二个日期, 格式: %Y%m%d

    Returns:
        如果 date1 < date2, 返回 -1.
        如果 date1 == date2, 返回 0.
        如果 date1 > date2, 返回 1.
    """
    date_format = "%Y%m%d"
    date1 = datetime.strptime(date1, date_format)
    date2 = datetime.strptime(date2, date_format)
    if date1 < date2:
        return -1
    elif date1 > date2:
        return 1
    else:
        return 0

"""
获取过去的 N 个交易日.
"""
def get_last_N_trade_date(num: int, begin: str = today()) -> List[str]:
    url = f"https://gateway.jrj.com/quot-kline?format=json&securityId=1000001&type=day&direction=left&range.num={num}&range.begin={begin}"
    log.info(f"查询最近的交易日, URL: {url}")
    result = []
    response = requests.get(url)
    if response.status_code == 200:
        content = response.json()
        log.info("查询交易日信息成功!")
        data = [StockHangQingInfo(code="000001", **item) for item in content["data"]["kline"]]
        result = [f"{d.index}" for d in data]
        return result
    else:
        log.error(f"请求失败，状态码: {response.status_code}")

"""
获取交易日验证器材.

@param start: 起始日期
@param end: 结束日期
"""
def trade_day_validator(start: str, end: str):
    # 将日期字符串转换为datetime对象
    date1_obj = datetime.strptime(start, "%Y%m%d")
    date2_obj = datetime.strptime(end, "%Y%m%d")
    # 计算两个日期之间的差异
    date_diff = date2_obj - date1_obj
    # 从timedelta对象中获取天数
    days_diff = date_diff.days
    trade_date_list = get_last_N_trade_date(days_diff + 1, end)
    log.info(f"交易日列表: {trade_date_list}")
    log.info(f"一共 {len(trade_date_list)} 个交易日")
    return lambda x: x in trade_date_list

"""
A date iterator between start and end.

@param start: 起始日期 (包含)
@param end: 结束日期 (不包含)
@param format: 日期格式, 默认 %Y%m%d
@param validator: 日期校验器. 若是设置了, 则每次获取到下一个日期后都进行校验, 校验失败继续取下一个.
"""
class DateIterator:
    def __init__(self, start: str, end: str, format: str = "%Y%m%d", validator=lambda x: True) -> None:
        self.format = format
        self.start = datetime.strptime(start, format)
        self.end = datetime.strptime(end, format)
        self.date = self.start - timedelta(days=1)
        self.validator = validator

    def next(self):
        # 移动到下一个值
        while self.has_next():
            self.date = self.date + timedelta(days=1)
            if self.validator(self.date.strftime(self.format)):
                break
        return self.date.strftime(self.format)
    
    def prev(self):
        # 移动到下一个值
        while self.has_prev():
            self.date = self.date - timedelta(days=1)
            if self.validator(self.date.strftime(self.format)):
                break
        return self.date.strftime(self.format)
    
    def has_next(self):
        return self.date < self.end;

    def has_prev(self):
        return self.date > self.start;

if __name__ == '__main__':
    for t in [1726191000, 1722821460, 1722821520, 1726124340]:
        print(timestamp_to_datetime(t))