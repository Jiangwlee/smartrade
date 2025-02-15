"""
blocktop
=============

同花顺最强板块.

Functions:
-----------
TBD

Usage:
------
TBD

Author:
-------
Bruce Li (jiangwlee@163.com)

Version:
--------
0.0.1
"""

import requests
from typing import List
from crawlers.utils.logger import get_logger
from crawlers.utils.dateutil import today
from crawlers.ths.dto import TopBlocksInfo
from crawlers.crawler import CrawlerBase

log = get_logger()

"""
最强板块爬虫
"""
class TopBlockCrawler(CrawlerBase):
    def __init__(self, datestr: str = today()) -> None:
        self.url = f"http://data.10jqka.com.cn/dataapi/limit_up/block_top?filter=HS,GEM2STAR&date={datestr}"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def crawl(self) -> List[TopBlocksInfo]:
        log.info(f"爬取最强板块, URL: {self.url}")
        response = requests.get(self.url, headers=self.headers)

        if response.status_code == 200:
            content = response.json()
            log.info("爬取最强板块数据成功!")
            data = [TopBlocksInfo(**item) for item in content["data"]]
            log.info(f"最强板块数量: {len(data)}")
            return data
        else:
            log.error(f"请求失败，状态码: {response.status_code}")

if __name__ == '__main__':
    spider = TopBlockCrawler()
    result = spider.crawl()
    for item in result:
        print(f"板块：{item.name}, 涨停数量: {item.limit_up_num}")