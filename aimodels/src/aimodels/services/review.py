"""
复盘服务.
"""
from crawlers.db.connector import getConnection
from aimodels.utils.logger import get_logger

log = get_logger()

def get_limitup_ladder(date: str):
    query = (
        "SELECT continue_num, GROUP_CONCAT(name) "
        "FROM smartrade.limit_up_ladder lul "
        "WHERE `date` = %s "
        "GROUP BY continue_num "
        "ORDER BY continue_num DESC ;")
    try:
        with getConnection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (date,))
                result = cursor.fetchall()
                return [{
                    "height": item[0],
                    "stocks": item[1].split(',')
                } for item in result]
    except Exception as ex:
        log.error(ex)

def get_leading_stock(date: str):
    """
    获取最高连板股.
    """
    query = (
        "SELECT DATE_FORMAT(date, '%Y%m%d') as `date`, continue_num, GROUP_CONCAT(name) AS names "
        "FROM smartrade.limit_up_ladder lul "
        "WHERE `date` >= %s - INTERVAL 100 DAY AND `date` <= %s "
        "GROUP BY `date`, continue_num "
        "HAVING continue_num = ( "
        "SELECT MAX(continue_num) "
        "FROM smartrade.limit_up_ladder "
            "WHERE `date` = lul.`date` "
        ") "
        "ORDER BY `date` DESC "
        "LIMIT 30;")
    try:
        with getConnection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (date, date))
                result = cursor.fetchall()
                resp = [{
                    "date": item[0],
                    "continuous_num": item[1],
                    "stocks": item[2]
                } for item in result]
                return sorted(resp, key=lambda x: x["date"], reverse=False)
    except Exception as ex:
        log.error(ex)