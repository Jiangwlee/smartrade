"""
复盘服务.
"""
import re
from collections import defaultdict
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

def get_zdt_stats_by_tag(date: str, tag: str):
    """
    获取过去30个交易日的涨跌停统计.
    """
    query = (
        "SELECT DATE_FORMAT(`date`, '%Y%m%d'), tag, COUNT(*), GROUP_CONCAT(name) "
        "FROM zdt_hangqing zh "
        "WHERE tag = %s AND `date` >= %s - INTERVAL 60 DAY AND `date` <= %s "
        "GROUP BY `date`"
    )
    try:
        with getConnection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (tag, date, date))
                result = cursor.fetchall()
                dates = [x[0] for x in result]
                dates = dates[-30:]
                result = [x for x in result if x[0] in dates]
                return result
    except Exception as ex:
        log.error(ex)

def get_zdt_stats(date: str):
    yz = get_zdt_stats_by_tag(date, '一字板')
    tz = get_zdt_stats_by_tag(date, 'T字板')
    td = get_zdt_stats_by_tag(date, '天地板')
    dt = get_zdt_stats_by_tag(date, '地天板')
    zt = get_zdt_stats_by_tag(date, '涨停')
    result = {}
    for item in zt:
        result[item[0]] = {
            'date': item[0],
            '涨停': item[2],
            '一字板': 0,
            'T字板': 0,
            '天地板': 0,
            '地天板': 0,
            '天地板股票': '',
            '地天板股票': ''
        }
    for item in yz:
        result[item[0]]['一字板'] = item[2]
    for item in tz:
        if item[0] in result:
            result[item[0]]['T字板'] = item[2]
    for item in td:
        if item[0] in result:
            result[item[0]]['天地板'] = item[2]
            result[item[0]]['天地板股票'] = item[3]
    for item in dt:
        if item[0] in result:
            result[item[0]]['地天板'] = item[2]
            result[item[0]]['地天板股票'] = item[3]
    return list(result.values())

def get_emotion_trend(date: str):
    """
    获取过去30个交易日的情绪变化趋势.
    """
    query = ("SELECT DATE_FORMAT(date, '%Y%m%d') as `date`, continue_num as continue_num, COUNT(*) as limit_up_count "
        "FROM smartrade.limit_up_ladder lul  "
        "WHERE `date` >= %s - INTERVAL 60 DAY AND `date` <= %s "
        "GROUP BY `date`,continue_num "
        "UNION "
        "SELECT DATE_FORMAT(date, '%Y%m%d') as `date`, 0 as continue_num, COUNT(*) as limit_up_count "
        "FROM smartrade.limit_up_stocks lus "
        "WHERE `date` >= %s - INTERVAL 60 DAY AND `date` <= %s "
        "GROUP BY `date` "
        "ORDER BY `date` DESC, continue_num DESC "
    )
    try:
        with getConnection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (date, date, date, date))
                result = cursor.fetchall()
                dataset = [
                    {
                        "date": x[0],
                        "height": x[1],
                        "count": x[2]
                    } for x in result
                ]
                # Initialize a defaultdict to organize data by date.
                organized_data = defaultdict(lambda: [0] * 20)

                # Process each entry in the input data.
                for entry in dataset:
                    date = entry['date']
                    height = entry['height']
                    count = entry['count']
                    organized_data[date][height] = count

                # Convert organized data into the desired format.
                result = []
                for date, counts in sorted(organized_data.items()):
                    counts[1] = counts[0] - sum(counts[2:])
                    row = [date] + counts
                    result.append(row)
                
                # 计算连板晋级率
                upRatio = []
                for i in range(0, len(result) - 1):
                    day1 = result[i][2:]
                    day2 = result[i + 1][2:]
                    ratio = []
                    for j in range(0, len(day1) - 1):
                        r = round(100 * day2[j + 1] / day1[j], 2) if day1[j] != 0 else '-'
                        ratio.append(r)
                    upRatio.append([result[i + 1][0], *ratio])
                # Print the output.
                return upRatio[-30:]
    except Exception as ex:
        log.error(ex)

def get_emotion_index(date: str, n: int):
    """
    获取情绪指标.
    """
    query_tdb = (
        "SELECT COUNT(*), GROUP_CONCAT(name) "
        "FROM zdt_hangqing "
        "WHERE date = %s AND tag = '天地板' "
    )
    query_dtb = (
        "SELECT COUNT(*), GROUP_CONCAT(name) "
        "FROM zdt_hangqing "
        "WHERE date = %s AND tag = '地天板' "
    )
    query_height = (
        "SELECT continue_num, COUNT(*), GROUP_CONCAT(name) "
        "FROM limit_up_ladder lul "
        "WHERE `date` = %s "
        "GROUP BY continue_num "
        "ORDER BY continue_num DESC "
        "LIMIT 1 "
    )
    query_limit_down = (
        "SELECT `date`, COUNT(*), GROUP_CONCAT(name) "
        "FROM limit_down_stocks lds "
        "WHERE `date` <= %s " 
        "GROUP BY `date` "
        "ORDER BY `date` DESC "
        "LIMIT 2"
    )
    query_limit_up = (
        "SELECT COUNT(*)"
        " FROM limit_up_ladder lul"
        " WHERE `date` = %s "
    )
    
    dates = get_last_N_trade_dates(n, date)
    result_list = []
    try:
        for d in dates:
            ret = {
                "date": d,
                "tdb_count": 0, # 天地板数量
                "tdb_stock": '', # 天地板个股
                "height": 0, # 连板高度
                "height_stock": '', # 最高连板股票
                "dt_count": 0, # 跌停数量
                "dt_continue_count": 0, # 连续跌停
                "dt_continue_stock": '', # 连续跌停个股
                "zt_continue_count": 0, # 连板数量
                "dtb_count": 0, # 地天板数量
                "dtb_stock": '', # 地天板个股
            }
            with getConnection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query_tdb, (d,))
                    result = cursor.fetchall()
                    if len(result) > 0:
                        ret["tdb_count"] = result[0][0]
                        ret["tdb_stock"] = result[0][1] if result[0][0] > 0 else ''

                    cursor.execute(query_dtb, (d,))
                    result = cursor.fetchall()
                    if len(result) > 0:
                        ret["dtb_count"] = result[0][0]
                        ret["dtb_stock"] = result[0][1] if result[0][0] > 0 else ''

                    # 查询连板高度
                    cursor.execute(query_height, (d,))
                    result = cursor.fetchall()
                    if len(result) > 0:
                        ret["height"] = result[0][0]
                        ret["height_stock"] = result[0][2]

                    # 查询跌停信息
                    cursor.execute(query_limit_down, (d,))
                    result = cursor.fetchall()
                    if len(result) > 1:
                        ret["dt_count"] = result[0][1]
                        cur_dt = result[0][2].split(',')
                        prev_dt = result[1][2].split(',')
                        intersection_list = list(set(cur_dt) & set(prev_dt))
                        ret["dt_continue_count"] = len(intersection_list)
                        ret["dt_continue_stock"] = ','.join(intersection_list)

                    # 查询连板个股
                    cursor.execute(query_limit_up, (d,))
                    result = cursor.fetchall()
                    if len(result) > 0:
                        ret["zt_continue_count"] = result[0][0]
            result_list.append(ret)
        return(result_list)
    except Exception as ex:
        log.error(ex)

def get_last_N_trade_dates(num: int, date: str):
    query = (
        "SELECT DISTINCT `date` "
        "FROM limit_up_ladder lul "
        "WHERE `date` <= %s "
        "ORDER BY `date` DESC "
        "LIMIT %s "
    )
    try:
        with getConnection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (date, num))
                dates = [x[0].strftime("%Y%m%d") for x in cursor.fetchall()]
                dates.reverse()
                return dates
    except Exception as ex:
        log.error(ex)

if __name__ == '__main__':
    get_emotion_index('20241216')