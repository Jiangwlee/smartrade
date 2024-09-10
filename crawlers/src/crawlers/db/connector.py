import mysql.connector
from mysql.connector.pooling import PooledMySQLConnection 
from crawlers.config import DB_CONFIG

from crawlers.utils.logger import getLogger

log = getLogger()

# 连接到 MySQL 数据库
connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="smartrade_db_pool",
    pool_size=10,
    pool_reset_session=True,
    **DB_CONFIG
)



# 获取连接
def getConnection() -> PooledMySQLConnection:
    return connection_pool.get_connection()
