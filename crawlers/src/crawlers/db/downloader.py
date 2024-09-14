"""
行情下载器.
"""

from crawlers.utils.logger import getLogger
from crawlers.utils.dateutil import today, DateIterator
from crawlers.ths.limitup import LimitUpCrawler
from crawlers.ths.limitdown import LimitDownCrawler
from crawlers.ths.limitupladder import LimitUpLadderCrawler
from crawlers.ths.blocktop import TopBlockCrawler
from crawlers.db.dao import LimitUpDao, LimitDownkDao, LimitUpLadderDao, TopBlockDao, TopBlockStocksDao

log = getLogger()

class Downloader:
    def __init__(self, start, end=today()) -> None:
        self.start_date = start
        self.end_data = end

    def run(self):
        date_iter = DateIterator(self.start_date, self.end_data)
        cur_date = self.start_date
        while True:
            spider_dao_list = [
                (LimitUpCrawler(cur_date), [LimitUpDao()]),
                (LimitDownCrawler(cur_date), [LimitDownkDao()]),
                (LimitUpLadderCrawler(cur_date), [LimitUpLadderDao()]),
                (TopBlockCrawler(cur_date), [TopBlockDao(), TopBlockStocksDao()])
            ]


            log.info(f"------------------------------------ [{cur_date}] ------------------------------------")
            for spider, dao_list in spider_dao_list:
                result = spider.crawl()
                for dao in dao_list:
                    dao.deleteByDate(cur_date)
                    dao.insert(cur_date, result)
                    log.info("-" * 20)
            # 更新日期
            if date_iter.hasNext():
                cur_date = date_iter.next()
            else:
                break

if __name__ == '__main__':
    downloader = Downloader('20240912', '20240913')
    downloader.run()