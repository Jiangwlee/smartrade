"""涨停个股服务.
"""
from typing import List
from crawlers.services.dto import LimitUpDetailsDto, BlockSummayDto
from crawlers.utils.logger import get_logger
from crawlers.utils.dbutil import rows_to_models
from crawlers.utils.dateutil import get_last_N_trade_date
from crawlers.db.connector import getConnection
from crawlers.eastmoney.stockrank import StockRankInfo, StockRankCrawler

log = get_logger()

def get_limitup_details(date: str) -> List[LimitUpDetailsDto]:
    """获取涨停个股行情. 
    
    Parameters:
        date: 日期, 格式: %YYYYMMDD, 比如: 20240101
        code: 股票代码
    
    Returns:
        LimitUpDetailsDto: 股票详情
    """
    log.info(f"正在查询股票详情")
    trade_date = get_last_N_trade_date(1, date)[0]
    query = ("SELECT "
                "s.`code` as code,"
                "s.name as name, "
                "s.`date` as date, "
                "s.currency_value as currency_value, "
                "s.turnover_rate as turnover_rate," 
                "s.first_limit_up_time as first_limit_up_time," 
                "s.last_limit_up_time as last_limit_up_time,"
                "s.open_num as open_num ,"
                "s.limit_up_type  as limit_up_type,"
                "s.order_volume as order_volume,"
                "s.order_amount as order_amount,"
                "s.high_days as high_days,"
                "tbs.reason_type as reason_type,"
                "tbs.reason_info as reason_info,"
                "tbs.block_ids as block_ids "
            "FROM limit_up_stocks s "
            "LEFT JOIN top_block_stocks tbs ON s.`date` = tbs.`date` AND s.code = tbs.code " 
            "WHERE s.`date` = %s;")
    try:
        stock_list = []
        with getConnection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (trade_date,))
                result = cursor.fetchall()
                print(result)
                if result != None and len(result) > 0:
                    stock_list = rows_to_models(result, LimitUpDetailsDto)
        block_list = get_block_summary(trade_date)
        block_map = {obj.code: obj for obj in block_list}
        for s in stock_list:
            for b in s.block_ids.split(','):
                if b in block_map:
                    s.blocks.append(block_map[b])
        return stock_list
    except Exception as ex:
        log.error(ex)

def get_block_summary(date) -> List[BlockSummayDto]:
    """获取板块概要.

    Parameters:
        date: 日期, 格式: %YYYYMMDD, 比如: 20240101
    
    Returns:
        BlockSummayDto: 板块概要信息.
    """
    log.info(f"正在查询板块概要")
    query = (
        "SELECT code, name, `date`, change_rate, limit_up_num, high, stock_list, ROW_NUMBER () OVER (ORDER BY limit_up_num DESC) AS rank_position "
        "FROM top_block tb "
        "WHERE `date` = %s;")
    try:
        with getConnection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (date,))
                result = cursor.fetchall()
                print(result)
                if result != None and len(result) > 0:
                    return rows_to_models(result, BlockSummayDto)
                else:
                    return []
    except Exception as ex:
        log.error(ex)

def get_eastmoney_rank() -> List[StockRankInfo]:
    """获取东方财富人气排名.
    
    Returns:
        StockRankInfo: 东方财富人气排名.
    """
    log.info("正在查询东方财富实时人气排名")
    spider = StockRankCrawler()
    return spider.crawl()

if __name__ == '__main__':
    print(get_eastmoney_rank())