"""
金融界龙虎榜爬虫
"""

import requests, json
from enum import Enum
from typing import List
from crawlers.jrj.dto import LongHuItem, LongHuInfo
from crawlers.crawler import CrawlerBase
from crawlers.utils.logger import get_logger
from crawlers.utils.dbutil import rows_to_models
from crawlers.db.dao import BrokerBranchDao

log = get_logger()

class LonghuCrawler(CrawlerBase):
    """
    金融界龙虎榜爬虫. 爬取营业部最近20个交易日的龙虎榜.

    Returns:
    {
        "游资姓名": List[]
    }
    """
    def __init__(self) -> None:
       self.brokers = BrokerBranchDao().fetch_all() # 营业部列表
       self.url = f"https://gateway.jrj.com/quot-dc/lhb/branchhis"
        

    def crawl(self) -> List[LongHuInfo]:
        result = []
        print(self.brokers)
        for broker in self.brokers:
            log.info(f"金融界龙虎榜行情, URL: {self.url}, 营业部：{broker[1]}")
            longhuList = []
            payload = {"activeName":"his","stattype":"3d","branchCode":broker[0],"pageNum":1,"pageSize":20}
            response = requests.post(self.url, json=payload)
            if response.status_code == 200:
                content = response.json()
                for data in content['data']['list']:
                    longhuitem = LongHuItem(**data)
                    longhuList.append(longhuitem)
                result.append(LongHuInfo(name=broker[2], items=longhuList))
            else:
                log.error(f"请求失败，状态码: {response.status_code}")
        return result


if __name__ == '__main__':
    spider = LonghuCrawler()
    result = spider.crawl()
    # for longhu in result:
    #     print(longhu.model_dump_json())
