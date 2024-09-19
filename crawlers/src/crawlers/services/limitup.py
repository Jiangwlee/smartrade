"""涨停个股服务.
"""
from typing import List
from crawlers.services.dto import LimitUpDetailsDto
from crawlers.utils.logger import get_logger
from crawlers.utils.dbutil import rows_to_models
from crawlers.db.connector import getConnection

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
        with getConnection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (date,))
                result = cursor.fetchall()
                print(result)
                if result != None and len(result) > 0:
                    return rows_to_models(result, LimitUpDetailsDto)
                else:
                    return []
    except Exception as ex:
        log.error(ex)

if __name__ == '__main__':
    print(get_limitup_details('20240918'))