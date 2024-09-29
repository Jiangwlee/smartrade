"""
复盘服务.
"""
import re
from crawlers.db.connector import getConnection
from aimodels.utils.logger import get_logger

log = get_logger()

def get_latest_date():
    query = (
        "SELECT DATE_FORMAT(date, '%Y%m%d') "
        "FROM smartrade.limit_up_ladder lul "
        "ORDER BY date DESC "
        "LIMIT 1;")
    try:
        with getConnection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return result[0][0]
    except Exception as ex:
        log.error(ex)

def get_limitup_ladder(date: str):
    query = (
        "SELECT continue_num, GROUP_CONCAT(name), GROUP_CONCAT(code) "
        "FROM smartrade.limit_up_ladder lul "
        "WHERE `date` = %s "
        "GROUP BY continue_num "
        "ORDER BY continue_num DESC ;")
    try:
        with getConnection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (date,))
                result = cursor.fetchall()
                ret = []
                for item in result:
                    stocks = item[1].split(',')
                    codes = item[2].split(',')
                    stock_objs = map(lambda s, c: {"name": s, "code": c}, stocks, codes)
                    ret.append({"height": item[0], "stocks": list(stock_objs)})
                return ret
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

def get_top_block_details(date: str):
    """
    返回 Top6 板块详情.
    """
    query = (
        "SELECT name, change_rate, limit_up_num, continuous_plate_num, high, stock_list "
        "FROM smartrade.top_block as tb "
        "WHERE `date` = %s "
        "ORDER BY limit_up_num DESC "
        "LIMIT 6;")
    try:
        with getConnection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (date,))
                result = cursor.fetchall()
                block_details = []
                for item in result:
                    top_stocks = get_top_stock_limitup_details(date, item[-1])
                    block_info = {
                        "name": item[0],
                        "change_rate": item[1],
                        "limit_up_num": item[2],
                        "continuous_plate_num": item[3],
                        "high": item[4],
                    }
                    for i in range(len(top_stocks)):
                        block_info[f"top{i}"] = top_stocks[i]["name"]
                    block_details.append(block_info)
                return block_details
    except Exception as ex:
        log.error(ex)

def get_top_stock_limitup_details(date: str, codes: str):
    """
    返回板块内 Top 领涨个股详情.
    """
    code_list = codes.split(',')
    # 动态生成多个 %s 占位符，长度与 code_list 相同
    placeholders = ','.join(['%s'] * len(code_list))
    query = (
        "SELECT name, high_days "
        "FROM smartrade.limit_up_stocks lus "
        "WHERE `date` = %s AND high_days LIKE '%天%板' AND `code` IN ({})"
        .format(placeholders))
    try:
        with getConnection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, [date] + code_list)
                result = cursor.fetchall()
                details = []
                for item in result:
                    numbers = re.findall(r'\d+', item[1]) # 从 "4天4板" 中提取出数字
                    details.append({
                        "name": f"{item[0]}: {item[1]}",
                        "days": numbers[0],
                        "limit_up_days": numbers[1]
                    })
                sorted_details = sorted(details, key=lambda x: (x['limit_up_days'], x['days']), reverse=True)
                return sorted_details[:3] if len(sorted_details) > 3 else sorted_details
    except Exception as ex:
        log.error(ex)

def get_limit_up_down_trend(date: str):
    limit_up_query = (
        "SELECT DATE_FORMAT(date, '%Y%m%d') as `date`, COUNT(*) as limit_up_count "
        "FROM smartrade.limit_up_stocks lus "
        "WHERE `date` >= %s - INTERVAL 100 DAY AND `date` <= %s "
        "GROUP BY `date` "
        "ORDER BY `date` DESC "
        "LIMIT 30; "
    )
    limit_down_query = (
        "SELECT DATE_FORMAT(date, '%Y%m%d') as `date`, COUNT(*) as limit_down_count "
        "FROM smartrade.limit_down_stocks lus "
        "WHERE `date` >= %s - INTERVAL 100 DAY AND `date` <= %s "
        "GROUP BY `date` "
        "ORDER BY `date` DESC "
        "LIMIT 30; "
    )
    try:
        with getConnection() as connection:
            dates = ['日期']
            limitup = ['涨停']
            limitdown = ['跌停']
            with connection.cursor() as cursor:
                cursor.execute(limit_up_query, (date, date))
                result = cursor.fetchall()
                sorted_result = sorted(result, key=lambda x: x[0], reverse=False)
                dates.extend([x[0] for x in sorted_result])
                limitup.extend([x[1] for x in sorted_result])
            with connection.cursor() as cursor:
                cursor.execute(limit_down_query, (date, date))
                result = cursor.fetchall()
                limit_down_map = {}
                for k, v in result:
                    limit_down_map[k] = v
                for d in dates[1:]:
                    if d in limit_down_map.keys():
                        limitdown.append(0 - limit_down_map[d])
                    else:
                        limitdown.append(0)
            ret = [dates, limitup, limitdown]
            return ret
    except Exception as ex:
        log.error(ex)

def get_top_stocks(date: str):
    """
    获取过去 100 个自然日中涨停次数最多的股票.
    """
    query = (
        "SELECT code, name, COUNT(*) as limit_down_count, GROUP_CONCAT(high_days) as high_days, DATE_FORMAT(MAX(`date`), '%Y%m%d') as latest_limit_up_date, DATE_FORMAT(MIN(`date`), '%Y%m%d') as first_limit_up_date, DATEDIFF(MAX(`date`), MIN(`date`)) as date_diff "
        "FROM smartrade.limit_up_stocks lus "
        "WHERE `date` >= %s - INTERVAL 100 DAY AND `date` <= %s "
        "GROUP BY `code`, `name` "
        "ORDER BY limit_down_count DESC "
        "LIMIT 30;"
    )
    try:
        with getConnection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (date, date))
                result = cursor.fetchall()
                return [
                    {
                        "code": x[0],
                        "name": x[1],
                        "count": x[2],
                        "high": get_high_days(x[3]),
                        'last': x[4],
                        'first': x[5],
                        'duration': x[6]
                    } for x in result
                ]
    except Exception as ex:
        log.error(ex)

def get_high_days(high_days_str: str):
    parts = high_days_str.split(",")
    high = 0
    high_days = '首板'
    for p in parts:
        numbers = re.findall(r'\d+', p)
        if len(numbers) == 2 and int(numbers[1]) > high:
            high_days = p
    return high_days