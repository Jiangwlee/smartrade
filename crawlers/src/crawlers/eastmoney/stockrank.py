"""
股吧人气排行
"""

import requests
from typing import List
from crawlers.eastmoney.dto import StockRankInfo
from crawlers.crawler import CrawlerBase
from crawlers.utils.logger import get_logger

log = get_logger()

class StockRankCrawler(CrawlerBase):
    def __init__(self) -> None:
       self.url = "https://emappdata.eastmoney.com/stockrank/getAllCurrentList"
       self.params = {"appId":"appId01","globalId":"786e4c21-70dc-435a-93bb-38","marketType":"","pageNo":1,"pageSize":100}

    def crawl(self) -> List[StockRankInfo]:
        response = requests.post(self.url, json=self.params)
        if response.status_code == 200:
            content = response.json()
            log.info("爬取东方财富人气榜数据成功!")
            data = [StockRankInfo(**item) for item in content["data"]]
            log.info(f"人气榜数量: {len(data)}")
            return data
        else:
            log.error(f"请求失败，状态码: {response.status_code}")


if __name__ == '__main__':
    spider = StockRankCrawler()
    result = spider.crawl()
    for item in result:
        print(item.sc)
