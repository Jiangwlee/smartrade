"""
一周涨幅排行
"""

import requests
from bs4 import BeautifulSoup
from typing import List
from dto import ChangeRankInfo
from crawlers.crawler import CrawlerBase
from crawlers.utils.logger import get_logger

log = get_logger()

class ChangeRankCrawler(CrawlerBase):
    def __init__(self) -> None:
       self.url = "https://q.stock.sohu.com/cn/jdph/jdph_shenshi_5d_00.shtml"

    def crawl(self) -> List[ChangeRankInfo]:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        try:
            response = requests.get(self.url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table', {'class': 'tableMSE'})
            
            if not table:
                return {"error": "Table not found"}
                
            stocks = []
            for row in table.find_all('tr')[1:]:  # Skip header row
                cols = row.find_all('td')
                if len(cols) >= 5:
                    name = cols[2].text.strip()
                    try:
                        garbled_str = name.encode('latin1')
                        name = garbled_str.decode('gbk')
                    except UnicodeEncodeError:
                        pass

                    stock = ChangeRankInfo(code=cols[1].text.strip(), name=name, change=cols[3].text.strip())
                    stocks.append(stock)        
            return stocks
            
        except requests.RequestException as e:
            return {"error": str(e)}


if __name__ == '__main__':
    # garbled_str = 'ÖÐ°Ù¼¯ÍÅ'.encode('latin1')

    # # 尝试以 GBK 解码
    # try:
    #     decoded_str = garbled_str.decode('gbk')
    #     print("解码为中文:", decoded_str)
    # except UnicodeDecodeError:
    #     print("无法用 GBK 解码")
    spider = ChangeRankCrawler()
    result = spider.crawl()
    print(result)
