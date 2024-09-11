"""
金融界行情爬虫
"""

import requests
from typing import List
from dto import StockHangQingInfo
from crawlers.crawler import CrawlerBase
from crawlers.utils.logger import getLogger

log = getLogger()

class HangQingCrawler(CrawlerBase):
    def __init__(self, code, range=60) -> None:
       self.code = code
       self.range = range
       self.security_id = f"1{code}" if code.startswith('6') else f"2{code}"
       self.url = f"https://gateway.jrj.com/quot-kline?format=json&securityId={self.security_id}&type=day&direction=left&range.num={self.range}"

    def crawl(self) -> List[StockHangQingInfo]:
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
    spider = HangQingCrawler(code='603883')
    result = spider.crawl()
    for item in result:
        print(item.code + ": " + str(item.open_price / 10000))
