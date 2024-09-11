"""
数据访问层.
"""

from connector import getConnection
from typing import List
from crawlers.utils.dateutil import timestampToDate
from crawlers.utils.logger import getLogger
from crawlers.ths.dto import LimitDownStockModel, LimitUpStockModel

log = getLogger()

class LimitDownkDao:
    def __init__(self) -> None:
        self.insert_query = ("INSERT INTO limit_down_stocks (code, name, change_rate, first_limit_down_time, last_limit_down_time, turnover_rate, currency_value) "
                             "VALUES (%s, %s, %s, %s, %s, %s, %s)")

    def insert(self, stocks: List[LimitDownStockModel]):
        try:
            data = [(s.code, s.name, s.change_rate, timestampToDate(s.first_limit_down_time), timestampToDate(s.last_limit_down_time), s.turnover_rate, s.currency_value) for s in stocks]
            with getConnection() as connection:
                with connection.cursor() as cursor:
                    cursor.executemany(self.insert_query, data)
                    connection.commit()
        except Exception as ex:
            log.error(ex)

class LimitUpDao:
    def __init__(self) -> None:
        self.insert_query = ("INSERT INTO limit_up_stocks (code, name, change_rate, first_limit_up_time, last_limit_up_time, turnover_rate, market_type, currency_value, open_num, limit_up_type, order_volume, order_amount, limit_up_suc_rate, reason_type, high_days) "
                             "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

    def insert(self, stocks: List[LimitUpStockModel]):
        try:
            data = [(s.code, s.name, 
                     s.change_rate, 
                     timestampToDate(s.first_limit_up_time), 
                     timestampToDate(s.last_limit_up_time), 
                     s.turnover_rate, 
                     s.market_type,
                     s.currency_value,
                     s.open_num,
                     s.limit_up_type,
                     s.order_volume,
                     s.order_amount,
                     s.limit_up_suc_rate,
                     s.reason_type,
                     s.high_days) for s in stocks]
            with getConnection() as connection:
                with connection.cursor() as cursor:
                    cursor.executemany(self.insert_query, data)
                    connection.commit()
        except Exception as ex:
            log.error(ex)


if __name__ == '__main__':
    from crawlers.ths.limitup import LimitUpCrawler
    spider = LimitUpCrawler('20240910')
    result = spider.crawl()
    dao = LimitUpDao()
    dao.insert(result.info)