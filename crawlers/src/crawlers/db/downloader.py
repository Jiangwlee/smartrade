"""
行情下载器.
"""

from crawlers.utils.logger import get_logger
from crawlers.utils.dateutil import today, trade_day_validator, DateIterator
from crawlers.ths.limitup import LimitUpCrawler
from crawlers.ths.limitdown import LimitDownCrawler
from crawlers.ths.limitupladder import LimitUpLadderCrawler
from crawlers.ths.blocktop import TopBlockCrawler
from crawlers.jrj.hangqing import HangQingCrawler, HangQingType
from crawlers.db.dao import LimitUpDao, LimitDownkDao, LimitUpLadderDao, TopBlockDao, TopBlockStocksDao, StockHangQingkDao

log = get_logger()

class Downloader:
    def __init__(self, start, end=today()) -> None:
        self.start_date = start
        self.end_data = end

    def run(self):
        validator = trade_day_validator(self.start_date, self.end_data)
        date_iter = DateIterator(self.start_date, self.end_data, validator=validator)
        next_date_iter = DateIterator(self.start_date, self.end_data, validator=validator)
        next_date_iter.next() # Move next_date_iter forward
        while date_iter.has_next():
            cur_date = date_iter.next()
            next_date = next_date_iter.next()
            spider_dao_list = [
                (LimitUpCrawler(cur_date), [LimitUpDao()]),
                (LimitDownCrawler(cur_date), [LimitDownkDao()]),
                (LimitUpLadderCrawler(cur_date), [LimitUpLadderDao()]),
                (TopBlockCrawler(cur_date), [TopBlockDao(), TopBlockStocksDao()])
            ]

            log.info(f"------------------------------------ [{cur_date}] ------------------------------------")
            # Crawl data of current date
            for spider, dao_list in spider_dao_list:
                result = spider.crawl()
                for dao in dao_list:
                    dao.deleteByDate(cur_date)
                    dao.insert(cur_date, result)
                    log.info("-" * 20)
            # Crawl data of next date
            limit_up_code_list = [(x[4], x[5]) for x in LimitUpDao().getItemsByDate(cur_date)]
            self.crawlHangQing(next_date, limit_up_code_list)

    def crawlHangQing(self, date: str, code_list: list):
        dao = StockHangQingkDao()
        dao.deleteByDate(date)
        for code, name in code_list:
            spider = HangQingCrawler(code, name, date, HangQingType.ONE_M, 1)
            result = spider.crawl()
            # Just keep the open and close hangqing
            result = [result[0], result[-1]]
            dao.insert(date, result)

if __name__ == '__main__':
    downloader = Downloader('20240101', '20240913')
    downloader.run()