"""
数据访问层.
"""

from abc import ABC, abstractmethod
from typing import List
from crawlers.db.connector import getConnection
from crawlers.utils.dateutil import timestamp_to_datetime
from crawlers.utils.logger import get_logger
from crawlers.ths.dto import LimitDownRespDataModel, LimitUpRespDataModel, LimitUpLadderInfo, TopBlocksInfo
from crawlers.jrj.dto import StockHangQingInfo

log = get_logger()

class BaseDao(ABC):
    def __init__(self, table: str):
        self._table = table
        self._delete_query = (f"DELETE FROM {self._table} WHERE date=%s")

    def deleteByDate(self, date: str):
        log.warning(f"Deleting data of {date} from table {self._table}")
        try:
            with getConnection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(self._delete_query, (date,))
                    connection.commit()
        except Exception as ex:
            log.error(ex)

    def getItemsByDate(self, date: str):
        log.info(f"正在查询 {self._table} 中 {date} 的记录")
        query = f"SELECT * FROM {self._table} WHERE date=%s"
        try:
            with getConnection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, (date, ))
                    return cursor.fetchall()
        except Exception as ex:
            log.error(ex)
    
    """
    Insert crawled data into database.
    """
    @abstractmethod
    def insert(self, date, crawl_result: any):
        pass

"""
跌停板数据库访问层 (Data Access Layer)
"""
class LimitDownkDao(BaseDao):
    def __init__(self) -> None:
        super().__init__("limit_down_stocks")
        self._insert_query = (f"INSERT INTO {self._table} (date, code, name, change_rate, first_limit_down_time, last_limit_down_time, turnover_rate, currency_value) "
                             "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")

    def insert(self, date: str, crawl_result: LimitDownRespDataModel):
        log.info(f"Inserting data into table {self._table}")
        try:
            data = [(date, s.code, s.name, s.change_rate, timestamp_to_datetime(s.first_limit_down_time), 
                     timestamp_to_datetime(s.last_limit_down_time), s.turnover_rate, s.currency_value) for s in crawl_result.info]
            with getConnection() as connection:
                with connection.cursor() as cursor:
                    cursor.executemany(self._insert_query, data)
                    connection.commit()
        except Exception as ex:
            log.error(ex)

"""
涨停板数据库访问层 (Data Access Layer)
"""
class LimitUpDao(BaseDao):
    def __init__(self) -> None:
        super().__init__("limit_up_stocks")
        self._insert_query = (f"INSERT INTO {self._table} (date, code, name, change_rate, first_limit_up_time, last_limit_up_time, turnover_rate, market_type, currency_value, open_num, limit_up_type, order_volume, order_amount, limit_up_suc_rate, reason_type, high_days) "
                             "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

    def insert(self, date: str, crawl_result: LimitUpRespDataModel):
        log.info(f"Inserting data into table {self._table}")
        try:
            data = [(date,
                     s.code, 
                     s.name, 
                     s.change_rate, 
                     timestamp_to_datetime(s.first_limit_up_time), 
                     timestamp_to_datetime(s.last_limit_up_time), 
                     s.turnover_rate, 
                     s.market_type,
                     s.currency_value,
                     s.open_num,
                     s.limit_up_type,
                     s.order_volume,
                     s.order_amount,
                     s.limit_up_suc_rate,
                     s.reason_type,
                     s.high_days) for s in crawl_result.info]
            with getConnection() as connection:
                with connection.cursor() as cursor:
                    cursor.executemany(self._insert_query, data)
                    connection.commit()
        except Exception as ex:
            log.error(ex)

"""
连板天梯数据库访问层 (Data Access Layer)
"""
class LimitUpLadderDao(BaseDao):
    def __init__(self) -> None:
        super().__init__("limit_up_ladder")
        self._insert_query = (f"INSERT INTO {self._table} (date, code, name, market_id, continue_num, height) "
                             "VALUES (%s, %s, %s, %s, %s, %s)")

    def insert(self, date:str, daily_ladder: List[LimitUpLadderInfo]):
        log.info(f"Inserting data into table {self._table}")
        try:
            data = []
            height = daily_ladder[0].height
            for ladder in daily_ladder:
                for item in ladder.code_list:
                    data.append((date, item.code, item.name, item.market_id, item.continue_num, height))
            with getConnection() as connection:
                with connection.cursor() as cursor:
                    cursor.executemany(self._insert_query, data)
                    connection.commit()
        except Exception as ex:
            log.error(ex)
    


"""
最强板块数据访问层(Data Access Layer)
"""
class TopBlockDao(BaseDao):
    def __init__(self):
        super().__init__("top_block")
        self._insert_query = (f"INSERT INTO {self._table} (date, code, name, change_rate, limit_up_num, continuous_plate_num, high, days, stock_list) "
                             "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
    
    def insert(self, date:str, top_blocks: List[TopBlocksInfo]):
        log.info(f"Inserting data into table {self._table}")
        try:
            data = [(date, t.code, t.name, t.change, t.limit_up_num, t.continuous_plate_num, t.high, t.days, ",".join([s.code for s in t.stock_list])) for t in top_blocks]
            with getConnection() as connection:
                with connection.cursor() as cursor:
                    cursor.executemany(self._insert_query, data)
                    connection.commit()
        except Exception as ex:
            log.error(ex)

"""
最强板块个股数据访问层(Data Access Layer)
"""
class TopBlockStocksDao(BaseDao):
    def __init__(self):
        super().__init__("top_block_stocks")
        self._insert_query = (f"INSERT INTO {self._table} (date, code, name, concept, reason_type, reason_info, block_ids, block_names) "
                             "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
    
    def insert(self, date:str, top_blocks: List[TopBlocksInfo]):
        log.info(f"Inserting data into table {self._table}")
        try:
            stock_dict = {}
            for b in top_blocks:
                for s in b.stock_list:
                    if s.code in stock_dict:
                        stock_dict[s.code]['block_ids'].append(b.code)
                        stock_dict[s.code]['block_names'].append(b.name)
                    else:
                        stock_dict[s.code] = {
                            "info": [date, s.code, s.name, s.concept, s.reason_type, s.reason_info],
                            "block_ids": [],
                            "block_names": []
                        }
            # 格式化成 VALUES
            data = []
            for s in stock_dict.values():
                s["info"].append(",".join(s["block_ids"]))
                s["info"].append(",".join(s["block_names"]))
                data.append(s["info"])

            with getConnection() as connection:
                with connection.cursor() as cursor:
                    cursor.executemany(self._insert_query, data)
                    connection.commit()
        except Exception as ex:
            log.error(ex)

"""
集合竞价数据访问层(Data Access Layer)
"""
class StockHangQingkDao(BaseDao):
    def __init__(self):
        super().__init__("stock_hangqing")
        self._insert_query = (f"INSERT INTO {self._table} (time, date, code, name, amount, volume, avg_price, high_price, low_price, open_price, close_price, pre_close_price) "
                             "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    
    def insert(self, date:str, hangqing_list: List[StockHangQingInfo]):
        log.info(f"Inserting data into table {self._table}")
        try:
            data = [(timestamp_to_datetime(s.time), date, s.code, s.name, s.amount, s.volume, s.avg_price, s.high_price, s.low_price, s.open_price, s.close_price, s.pre_close_price) for s in hangqing_list]
            with getConnection() as connection:
                with connection.cursor() as cursor:
                    cursor.executemany(self._insert_query, data)
                    connection.commit()
        except Exception as ex:
            log.error(ex)

    def getHangQingByDateAndCode(self, date: str, code: str):
        log.info(f"Selecting data from table {self._table} by date {date} and code {code}")
        query = f"SELECT code, name, UNIX_TIMESTAMP(time), 0, amount, volume, avg_price, high_price, low_price, open_price, close_price, pre_close_price FROM {self._table} WHERE `date` = %s AND code = %s"
        try:
            with getConnection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, (date, code))
                    return cursor.fetchall()
        except Exception as ex:
            log.error(ex)

if __name__ == '__main__':
    from crawlers.jrj.hangqing import HangQingCrawler, HangQingType
    date = '20240910'
    spider = HangQingCrawler('603883', '老百姓', '20240912', HangQingType.ONE_M, 1)
    result = spider.crawl()
    result = [result[0], result[-1]]
    dao = StockHangQingkDao()
    # dao.deleteByDate(date)
    # dao.insert(date, result)