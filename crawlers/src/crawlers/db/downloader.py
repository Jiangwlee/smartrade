"""
行情下载器.
"""

from crawlers.utils.logger import get_logger
from crawlers.utils.dateutil import today, trade_day_validator, get_last_N_trade_date, DateIterator
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
        cur_date = None
        while date_iter.has_next():
            # 如果第一次进入循环, 将 prev_date 设置为上一个交易日, 否则设置成上一个 cur_date, 然后更新 cur_date
            prev_date = cur_date if cur_date is not None else get_last_N_trade_date(1, self.start_date)
            cur_date = date_iter.next()
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
            # 获取上一个交易日的涨停板列表, 并抓取今日的竞价行情
            limit_up_code_list = [(x[4], x[5]) for x in LimitUpDao().getItemsByDate(prev_date)]
            self.__crawl_hang_qing(cur_date, limit_up_code_list)

    def __crawl_hang_qing(self, date: str, code_list: list):
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