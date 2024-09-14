"""
金融界行情爬虫
"""

import requests
from enum import Enum
from typing import List
from crawlers.jrj.dto import StockHangQingInfo
from crawlers.crawler import CrawlerBase
from crawlers.utils.logger import getLogger

log = getLogger()

"""
获取某一天的行情, 一分钟一条记录, 一共 241 条记录. 第一条记录是集合竞价记录, 最后一条记录是尾盘集合竞价.

@param code: 股票代码
@param date_str: 日期字符串, 比如: 20240909
"""
def getHangqingOfDate(code: str, date_str: str) -> List[StockHangQingInfo]:
    # 查询每天的1分钟级别 K 线数据，第一个记录就是集合竞价成交数据
    spider = HangQingCrawler(code, date_str, HangQingType.ONE_M, 1)
    result = spider.crawl()
    return result

class HangQingType(Enum):
    DAY = 0
    ONE_M = 1


class HangQingCrawler(CrawlerBase):
    """
    金融界行情爬虫. 爬取从某一天开始往前的 N 条行情记录

    @param code: 股票代码
    @param date: 行情开始日期
    @param type: 行情类型
    """
    def __init__(self, code, date: str, type: HangQingType, range=60) -> None:
       self.code = code
       self.range = range
       self.security_id = f"1{code}" if code.startswith('6') else f"2{code}"
       self.type_param_map = {
           HangQingType.DAY: "day",
           HangQingType.ONE_M: "1minkline",
       }
       self.type = type
       self.url = f"https://gateway.jrj.com/quot-kline?format=json&securityId={self.security_id}&type={self.type_param_map[self.type]}&direction=left&range.num={self.range}&range.begin={date}"
        

    def crawl(self) -> List[StockHangQingInfo]:
        log.info(f"金融界行情, URL: {self.url}")
        response = requests.get(self.url)
        if response.status_code == 200:
            content = response.json()
            log.info("爬取金融界行情数据成功!")
            data = [StockHangQingInfo(code=self.code, **item) for item in content["data"]["kline"]]
            log.info(f"K线数量: {len(data)}")
            return data
        else:
            log.error(f"请求失败，状态码: {response.status_code}")


if __name__ == '__main__':
    # 查询每天的1分钟级别 K 线数据，第一个记录就是集合竞价成交数据
    spider = HangQingCrawler('603883', '20240912', HangQingType.ONE_M, 1)
    result = spider.crawl()
    print(result[0])
