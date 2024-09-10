from connector import getConnection
from crawlers.utils.logger import getLogger

log = getLogger()

insert_query = "INSERT INTO stock (code, name) VALUES (%s, %s)"
delete_query = "DELETE FROM stock WHERE code=%s"


class StockDao:
    def insert(self, code: str, name: str):
        try:
            with getConnection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(insert_query, (code, name))
                    connection.commit()
        except Exception as ex:
            log.error(ex)

    def delete(self, code: str):
        try:
            with getConnection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(delete_query, (code,))
                    connection.commit()
        except Exception as ex:
            log.error(ex)
    

if __name__ == '__main__':
    dao = StockDao()
    dao.insert("000001", "Test")
    dao.delete("000001")