"""
limitdown
=============

本模块提供了同花顺跌停板数据的爬取方法.

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

import time
import requests
from datetime import date
from crawlers.utils.logger import getLogger
from crawlers.ths.dto import RespDataModel

log = getLogger()
base_url = "https://data.10jqka.com.cn/dataapi/limit_up/lower_limit_pool?limit=20&field=199112,10,330333,330334,1968584,3475914,9004"
url_formatter = "&page={page}&filter=HS,GEM2STAR&order_field=330334&order_type=0&date={today}&_={timestamp_milliseconds}"

def getUrl(page, date, timestamp):
    return base_url + url_formatter.format(page=page, today=date, timestamp_milliseconds=timestamp)

def crawlPage(page: int, result: list) -> RespDataModel:
    today = date.today().strftime("%Y%m%d")
    timestamp_milliseconds = int(time.time() * 1000)
    url = getUrl(page, today, timestamp_milliseconds)
    
    log.info(f"爬取跌停板数据, URL: {url}")
    response = requests.get(url)
    if response.status_code == 200:
        content = response.json()
        log.info("爬取跌停数据成功!")
        data = RespDataModel(**content["data"])
        log.info(f"跌停总数量: {data.page.total}")

        page_info = data.page
        result.extend(data.info)
        if page_info.page < page_info.count:
            log.info(f"一共 {page_info.count} 页，当前第 {page} 页")
            crawlPage(page + 1, result)
        else:
            log.info(f"一共 {page_info.total} 条跌停数据, 已经爬取 {len(result)} 条跌停数据")
        
        return data
    else:
        log.error(f"请求失败，状态码: {response.status_code}")

def crawl() -> RespDataModel:
    result_info = []
    total = crawlPage(1, result_info)
    total.info = result_info
    return total

if __name__ == '__main__':
    data = crawl()
    for item in data.info:
        print(item.name)
    print(f"跌停封板率: {data.limit_down_count.today.rate}")
    