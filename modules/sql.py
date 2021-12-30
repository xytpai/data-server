import pymysql


class SQLManager:
    def __init__(self, cfg, check=True) -> None:
        self.cfg = cfg
        self.conn = pymysql.connect(
            host=self.cfg.database.host,
            user=self.cfg.database.user,
            password=self.cfg.database.password,
            charset='utf8')
        if check:
            self.__check()

    def __del__(self):
        self.conn.close()

    def run(self, sequence: list, mechod='fetchone') -> list:
        try:
            self.conn.ping()
        except Exception as e:
            print(str(e))
            self.conn = self.conn = pymysql.connect(
                host=self.cfg.database.host,
                user=self.cfg.database.user,
                password=self.cfg.database.password,
                charset='utf8')
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

    def __check(self) -> None:
        info_head = 'SQLManager CK: '
        database_name = self.cfg.database.base
        table_dict = self.cfg.database.tables
        init_dict = self.cfg.database.init
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
