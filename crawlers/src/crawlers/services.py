"""
服务层: 封装主要业务逻辑.
"""

from db.downloader import Downloader

def download_one_day(date_str: str):
    """
    下载某一天的行情.
    --
    @param date_str: 日期. 格式为 %Y%m%d, 比如: 20240101
    """
    downloader = Downloader(date_str, date_str)
    downloader._crawl_hang_qing()