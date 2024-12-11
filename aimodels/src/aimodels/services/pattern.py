"""
形态（模式）识别.
"""
import re
from crawlers.db.connector import getConnection
from aimodels.utils.logger import get_logger

log = get_logger()

def get_reversal_stocks():
    """
    查询反包个股：涨停-断板-再涨停
    """
    query = ("WITH TopDates AS ( "
             "    SELECT DISTINCT `date` "
             "    FROM smartrade.limit_up_stocks lus "
             "    ORDER BY `date` DESC "
             "    LIMIT 3"
             "),"
             "AllDates AS ( "
             "    SELECT "
             "        MAX(`date`) AS D1, "
             "        MIN(`date`) AS D3, "
             "        (SELECT `date` FROM TopDates ORDER BY date DESC LIMIT 1 OFFSET 1) AS D2 "
             "    FROM TopDates "
             "), "
             "D2Values AS ( "
             "    SELECT code, name "
             "    FROM smartrade.limit_up_stocks "
             "    WHERE date = (SELECT D2 FROM AllDates) "
             "), "
             "D13Values AS ( "
             "    SELECT code, name "
             "    FROM smartrade.limit_up_stocks "
             "    WHERE date IN (SELECT D1 FROM AllDates UNION SELECT D3 FROM AllDates) "
             "    GROUP BY code, name "
             "    HAVING COUNT(DISTINCT `date`) = 2 "
             ") "
             "SELECT code, name "
             "FROM D13Values "
             "WHERE code NOT IN (SELECT code FROM D2Values);")

    try:
        with getConnection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return result
    except Exception as ex:
        log.error(ex)