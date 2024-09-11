"""
limitup
=============

本模块提供了同花顺涨停板数据的爬取方法.

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
from crawlers.utils.logger import getLogger
from crawlers.utils.dateutil import today, timestampInMilliseconds
from crawlers.ths.dto import LimitUpRespDataModel
from crawlers.crawler import CrawlerBase

log = getLogger()




class LimitUpCrawler(CrawlerBase):
    def __init__(self, date=today()) -> None:
        self.date = date
        self.base_url = "http://data.10jqka.com.cn/dataapi/limit_up/limit_up_pool?limit=20&field=199112,10,9001,330323,330324,330325,9002,330329,133971,133970,1968584,3475914,9003"
        self.url_formatter = "&page={page}&filter=HS,GEM2STAR&order_field=330324&order_type=0&date={date}&_={timestamp_milliseconds}"

    def getUrl(self, page, timestamp):
        return self.base_url + self.url_formatter.format(page=page, date=self.date, timestamp_milliseconds=timestamp)

    def crawlPage(self, page: int, result: list) -> LimitUpRespDataModel:
        url = self.getUrl(page, timestampInMilliseconds())
        
        log.info(f"爬取涨停板数据, URL: {url}")
        response = requests.get(url)
        if response.status_code == 200:
            content = response.json()
            log.info("爬取涨停数据成功!")
            data = LimitUpRespDataModel(**content["data"])
            log.info(f"涨停总数量: {data.page.total}")

            page_info = data.page
            result.extend(data.info)
            if page_info.page < page_info.count:
                log.info(f"一共 {page_info.count} 页，当前第 {page} 页")
                self.crawlPage(page + 1, result)
            else:
                log.info(f"一共 {page_info.total} 条涨停数据, 已经爬取 {len(result)} 条涨停数据")
            
            return data
        else:
            log.error(f"请求失败，状态码: {response.status_code}")
            
    def crawl(self) -> LimitUpRespDataModel:
        result_info = []
        total = self.crawlPage(1, result_info)
        total.info = result_info
        return total

if __name__ == '__main__':
    crawler = LimitUpCrawler()
    data = crawler.crawl()
    for item in data.info:
        print(item.name)
    print(f"涨停封板率: {data.limit_down_count.today.rate}")
    