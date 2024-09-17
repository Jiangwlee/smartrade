"""
数据集爬虫.
"""
import csv
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List
from crawlers.db.connector import getConnection
from crawlers.db.dao import LimitDownkDao, LimitUpDao
from crawlers.utils.logger import get_logger
from crawlers.utils.dateutil import today, previous_date, next_date, offset_in_minutes, trade_day_validator, DateIterator
from crawlers.utils.dbutil import rows_to_models
from crawlers.ths.blocktop import TopBlockCrawler
from crawlers.ths.limitupladder import LimitUpLadderCrawler
from crawlers.jrj.hangqing import getHangqingOfDate

log = get_logger()

"""
主要包含以下属性:
1. 昨日涨停属性
    1. 连板数: 当前是第几连板
    2. 总市值：单位 "亿"
    3. 流通值：单位 "亿"
    4. 封流比：封单金额和流通市值的比率
    5. 涨停打开次数：涨停后打开了几次
    6. 首次封板时间: 相对于 9:30 的分钟偏移
    7. 最后封板时间：相对于 9:30 的分钟偏移
    8. 换手率
2. 今日竞价属性
    1. 竞价涨幅
    2. 竞价成交金额 / 昨日封板金额

输出标签：
1. 涨停
2. 跌停
3. 上涨（未涨停）
4. 下跌（未跌停）
"""
class DatasetModel(BaseModel):
    ## 基本信息
    code: str
    name: str
    date: str
    ## 昨日涨停信息
    continuous_num: int = Field(..., description="昨天是第几连板")
    currency_value: float = Field(..., description="昨日收盘流通值")
    feng_liu_rate: float = Field(..., description="昨日封流比")
    limit_up_open: int = Field(..., description="昨日涨停打开次数")
    first_limit_up_time: int = Field(..., description="首次封板时间, 相对于 9:30 的分钟偏移")
    last_limit_up_time: int = Field(..., description="最后封板时间: 相对于 9:30 的分钟偏移")
    turnover_rate: float = Field(..., description="换手率")
    ## 今日行情信息
    open_strength: float = Field(..., description="竞价强度: 竞价成交量 / 昨日封板量")
    open_change: float = Field(..., description="开盘涨幅")
    close_change: float = Field(..., description="收盘涨幅")
    label: int = Field(..., description="标签(今日表现): 1. 涨停; 2. 跌停; 3. 上涨; 4. 下跌")

"""
数据集输出模型.
"""
class DatasetOutModel(BaseModel):
    continuous_num: int = Field(..., description="昨天是第几连板")
    currency_value: float = Field(..., description="昨日收盘流通值")
    feng_liu_rate: float = Field(..., description="昨日封流比")
    limit_up_open: int = Field(..., description="昨日涨停打开次数")
    first_limit_up_time: int = Field(..., description="首次封板时间, 相对于 9:30 的分钟偏移")
    last_limit_up_time: int = Field(..., description="最后封板时间: 相对于 9:30 的分钟偏移")
    turnover_rate: float = Field(..., description="换手率")
    ## 今日行情信息
    open_strength: float = Field(..., description="竞价强度: 竞价成交量 / 昨日封板量")
    open_change: float = Field(..., description="开盘涨幅")
    label: int = Field(..., description="标签(今日表现): 1. 涨停; 2. 跌停; 3. 上涨; 4. 下跌")

class ResultModel(BaseModel):
    code: str
    name: str
    currency_value: int
    first_limit_up_time: datetime
    last_limit_up_time: datetime
    turnover_rate: float
    limit_up_open: int
    order_volume: int = Field(..., description="封单量")
    order_amount: float = Field(..., description="封单金额")
    continuous_num: int
    height: int


SELECT_QUERY = """
SELECT 
    s.code as code, 
    s.name as name, 
    s.currency_value as currency_value,
    s.first_limit_up_time as first_limit_up_time, 
    s.last_limit_up_time as last_limit_up_time, 
    s.turnover_rate as turnover_rate, 
    s.open_num as  limit_up_open,
    s.order_volume as order_volume,
    s.order_amount as order_amount,
    COALESCE(l.continue_num, 1) as continuous_num, 
    COALESCE(l.height, (SELECT height FROM limit_up_ladder k WHERE k.`date` = %(date)s LIMIT 1)) as height 
FROM limit_up_stocks s 
LEFT JOIN limit_up_ladder l ON s.code = l.code AND s.`date` = l.`date` 
WHERE s.`date` = %(date)s;
"""

class DatasetDao():
    def selectByDate(self, date_str: str = today()):
        try:
            with getConnection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(SELECT_QUERY, {"date": date_str})
                    return cursor.fetchall()
        except Exception as ex:
            log.error(ex)

class DatasetGenerator():
    """
    数据集生成器.

    @param start: start date in format "%Y%m%d". Example: 20240101
    @param end: end date in format "%Y%m%d". Example: 20240101
    """
    def __init__(self, start: str, end: str) -> None:
        self.start = start
        self.end = end
        self.dataset = []

    def saveToCsv(self, data: List[BaseModel], filepath):
        with open(filepath, 'w', newline="", encoding="UTF-8") as csvfile:
            dicts = []
            for obj in data:
                obj.code = " " + obj.code
                dicts.append(obj.dict())
            writer = csv.DictWriter(csvfile, fieldnames=dicts[0].keys())
            writer.writeheader()
            writer.writerows(dicts)
            log.info(f"保存数据集至: {filepath}")

    def save(self, filepath: str):
        # output = [DatasetOutModel(**d.dict()) for d in self.dataset]
        # self.saveToCsv(output, filepath)
        # 保存原始数据，方便验证
        self.saveToCsv(self.dataset, f"{filepath}-raw.csv")
    
    def generate(self):
        self.dataset = []
        date_iter = DateIterator(self.start, self.end, validator=trade_day_validator(self.start, self.end))
        next_date_iter = DateIterator(self.start, self.end, validator=trade_day_validator(self.start, self.end))
        next_date_iter.next()

        while date_iter.has_next():
            log.info("-" * 50)
            # 涨停日期
            limit_up_day = date_iter.next()
            next_day = next_date_iter.next()
            log.info(f"[{limit_up_day}] 生成涨停股票数据集, 下一个交易日: {next_day}")
            # 涨停之后的一天，根据第二天的表现来打标签
            # 获取涨停日的信息
            dao = DatasetDao()
            limit_up_info = rows_to_models(dao.selectByDate(limit_up_day), ResultModel)

            # 获取第二天的信息
            dao = LimitUpDao()
            limit_up_list = dao.getItemsByDate(next_day)
            limit_up_code_list = [s[4] for s in limit_up_list]
            dao = LimitDownkDao()
            limit_down_list = dao.getItemsByDate(next_day)
            limit_down_code_list = [s[4] for s in limit_down_list]
            # 处理各个涨停的股票
            for r in limit_up_info:
                code = r.code
                name = r.name
                hangqing = getHangqingOfDate(code, name, next_day)
                # 集合竞价行情
                open = hangqing[0]
                # 开盘涨幅
                open_change = (open.close_price - open.pre_close_price) / open.pre_close_price
                # 竞价强度: 开盘成交量 / 昨日封单量
                open_strength = open.volume / r.order_volume
                # 当日最终收盘涨幅
                close = hangqing[-1]
                close_change = (close.close_price - open.pre_close_price) / open.pre_close_price
                # 最终标签
                label = 3 if close_change > 0 else 4
                # 查询涨停板和跌停板
                if code in limit_up_code_list:
                    label = 1
                else:
                    if code in limit_down_code_list:
                        label = 2

                self.dataset.append(
                    DatasetModel(
                        code=r.code,
                        name=r.name,
                        date=next_day,
                        continuous_num=r.continuous_num,
                        currency_value=r.currency_value / 100000000,
                        feng_liu_rate=r.order_amount / r.currency_value,
                        limit_up_open=r.limit_up_open,
                        first_limit_up_time=offset_in_minutes(r.first_limit_up_time),
                        last_limit_up_time=offset_in_minutes(r.last_limit_up_time),
                        turnover_rate=r.turnover_rate,
                        open_strength=open_strength,
                        open_change=open_change,
                        close_change=close_change,
                        label=label
                    )
                )
        log.info("涨停数据集生成完毕!")

if __name__ == '__main__':
    # generator = DatasetGenerator('20240501', '20240831')
    # generator = DatasetGenerator('20240101', '20240831')
    generator = DatasetGenerator('20240101', '20240831')
    generator.generate()
    generator.save("C:\\Users\\admin\\Downloads\\dataset-240101-240831.csv")