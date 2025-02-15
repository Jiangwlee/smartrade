"""
东方财富净流入、净流出榜
"""

import requests
import json
from typing import List
from dto import StockNetAmountInfo
from crawlers.crawler import CrawlerBase
from crawlers.utils.logger import get_logger
from crawlers.utils.dateutil import timestamp_in_milliseconds
from crawlers.utils.stringutil import generate_random_numeric_string

log = get_logger()

params = (
    "&fid=f62&pz=50&pn=1&np=1&fltt=2&invt=2&ut=b2884a393a59ad64002292a3e90d46a5"
    "&fs=m:0+t:6+f:!2,m:0+t:13+f:!2,m:0+t:80+f:!2,m:1+t:2+f:!2,m:1+t:23+f:!2,m:0+t:7+f:!2,"
    "m:1+t:3+f:!2&fields=f12,f14,f2,f3,f62,f184,f66,f69,f72,f75,f78,f81,f84,f87,f204,f205,f124,f1,f13"
    "&ut=b2884a393a59ad64002292a3e90d46a5"
)

class NetInOutCrawler(CrawlerBase):
    def __init__(self, isNetIn=True) -> None:
       self.query_id = f"jQuery{generate_random_numeric_string()}_{timestamp_in_milliseconds()}"
       self.isNetIn = isNetIn
       self.url = f"https://push2.eastmoney.com/api/qt/clist/get?cb={self.query_id}" + f"&po={1 if isNetIn else 0}" + params

    def crawl(self) -> List[StockNetAmountInfo]:
        log.info(self.url)
        response = requests.get(self.url)
        if response.status_code == 200:
            content = response.text
            jsonstr = content[len(self.query_id) + 1 : -2]
            if self.isNetIn:
                log.info(f"爬取东方财富净流入榜成功!")
            else:
                log.info(f"爬取东方财富净流出榜成功!")
            data = [StockNetAmountInfo(**item) for item in json.loads(jsonstr)['data']['diff']]
            log.info(f"人气榜数量: {len(data)}")
            return data
        else:
            log.error(f"请求失败，状态码: {response.status_code}")

if __name__ == '__main__':
    spider = NetInOutCrawler()
    for item in spider.crawl():
        print(item.name + ": " + str(item.net_amount))

    print("开始爬取流出榜")
    spider = NetInOutCrawler(isNetIn=False)
    for item in spider.crawl():
        print(item.name + ": " + str(item.net_amount))
