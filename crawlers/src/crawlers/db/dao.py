"""
数据访问层.
"""

from abc import ABC, abstractmethod
from typing import List
from crawlers.db.connector import getConnection
from crawlers.utils.dateutil import timestampToDatetime
from crawlers.utils.logger import getLogger
from crawlers.ths.dto import LimitDownRespDataModel, LimitUpRespDataModel, LimitUpLadderInfo, TopBlocksInfo

log = getLogger()

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

    def contains(self, date: str, code: str):
        log.info(f"检查 {self._table} 中 {date} 是否有关于 {code} 的记录")
        query = (f"SELECT COUNT(*) FROM {self._table} WHERE date=%s AND code=%s")
        try:
            with getConnection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, (date, code))
                    result = cursor.featchAll()
                    return result[0] > 0
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
            data = [(date, s.code, s.name, s.change_rate, timestampToDatetime(s.first_limit_down_time), 
                     timestampToDatetime(s.last_limit_down_time), s.turnover_rate, s.currency_value) for s in crawl_result.info]
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
                     timestampToDatetime(s.first_limit_up_time), 
                     timestampToDatetime(s.last_limit_up_time), 
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

if __name__ == '__main__':
    from crawlers.ths.blocktop import TopBlockCrawler
    date = '20240910'
    spider = TopBlockCrawler(date)
    result = spider.crawl()
    dao = TopBlockStocksDao()
    dao.deleteByDate(date)
    dao.insert(date, result)