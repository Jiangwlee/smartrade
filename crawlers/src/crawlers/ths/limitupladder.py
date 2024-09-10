"""
limitupladder
=============

同花顺连板天梯.

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
from crawlers.utils.logger import getLogger
from crawlers.utils.dateutil import today
from crawlers.ths.dto import LimitUpLadderInfo
from crawlers.crawler import CrawlerBase

log = getLogger()

class LimitUpLadderCrawler(CrawlerBase):
    def __init__(self) -> None:
        self.url = f"https://data.10jqka.com.cn/dataapi/limit_up/continuous_limit_up?filter=HS,GEM2STAR&date={today()}"

    def crawl(self) -> List[CrawlerBase]:
        response = requests.get(self.url)

        if response.status_code == 200:
            content = response.json()
            log.info("爬取连板天梯数据成功!")
            data = [LimitUpLadderInfo(**item) for item in content["data"]]
            log.info(f"连板天梯: {len(data)}")
            return data
        else:
            log.error(f"请求失败，状态码: {response.status_code}")


if __name__ == '__main__':
    spider = LimitUpLadderCrawler()
    result = spider.crawl()
    for item in result:
        print(f"连板高度：{item.height}, 涨停数量: {len(item.code_list)}")