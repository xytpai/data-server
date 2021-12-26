from config import cfg
import pymysql as sql


class SQLManager:
    def __init__(self) -> None:
        self.conn = sql.connect(
            host=cfg.database.host,
            user=cfg.database.user,
            password=cfg.database.password,
            charset='utf8')

    def __del__(self):
        self.conn.close()

    def run(self, sequence: list, mechod='fetchone') -> list:
        output = []
        cursor = self.conn.cursor()
        for item in sequence:
            cursor.execute(item)
            self.conn.commit()
            if mechod == 'fetchone':
                output.append(str(cursor.fetchone()))
            elif mechod == 'fetchall':
                output.append(str(cursor.fetchall()))
        return output
