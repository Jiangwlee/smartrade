"""
成交量排行
"""

"""
股吧人气排行
"""

import requests
from typing import List
from dto import AmountRankInfo
from crawlers.crawler import CrawlerBase
from crawlers.utils.logger import get_logger

log = get_logger()

class AmountRankCrawler(CrawlerBase):
    def __init__(self) -> None:
       self.url = "https://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=15&sort=amount&asc=0&node=hs_a&symbol="

    def crawl(self) -> List[AmountRankInfo]:
        response = requests.get(self.url)
        if response.status_code == 200:
            content = response.json()
            log.info("爬取新浪股票成交量数据成功!")
            data = [AmountRankInfo(**item) for item in content]
            log.info(f"成交榜榜数量: {len(data)}")
            return data
        else:
            log.error(f"请求失败，状态码: {response.status_code}")


if __name__ == '__main__':
    spider = AmountRankCrawler()
    result = spider.crawl()
    for item in result:
        print(item.name + ": " + str(item.amount / (100000000)) + " 亿, " + str(item.volume / 1000000) + " 万手")
