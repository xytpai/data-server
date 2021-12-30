import pymysql as sql
from config import cfg


class SQLManager:
    def __init__(self, check=True) -> None:
        self.conn = sql.connect(
            host=cfg.database.host,
            user=cfg.database.user,
            password=cfg.database.password,
            charset='utf8')
        if check:
            self.check()

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

    def check(self):
        info_head = 'SQLManager CK: '
        database_name = cfg.database.base
        table_dict = cfg.database.tables
        init_dict = cfg.database.init
        # database check
        try:
            self.run(["create database {0};".format(database_name)])
        except Exception as e:
            print(info_head + str(e))
        self.run(["use {0};".format(database_name)])
        # table check
        for name in table_dict.keys():
            params = ", ".join(table_dict[name])
            try:
                self.run(["create table {0}({1});".format(name, params)])
            except Exception as e:
                print(info_head + str(e))
        # init logic
        for name in init_dict.keys():
            for seq in init_dict[name]:
                params, values = [], []
                for item, param in zip(seq, table_dict[name]):
                    if item is not None:
                        params.append(param.split(' ')[0])
                        if isinstance(item, str):
                            values.append('\'' + item + '\'')
                        else:
                            values.append(str(item))  # number
                command = "insert into {0} ({1}) values ({2});".format(
                    name, ", ".join(params), ", ".join(values))
                try:
                    self.run([command])
                except Exception as e:
                    print(info_head + str(e))


class AuthorityManager:
    def __init__(self, sql_manager) -> None:
        self.sql_manager = sql_manager

    def authorize(self, user_id, command):
        return True
