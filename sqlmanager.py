import pymysql as sql
from config import cfg


class SQLManager:
    def __init__(self) -> None:
        self.conn = sql.connect(
            host=cfg.database.host,
            user=cfg.database.user,
            password=cfg.database.password,
            charset='utf8')
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
            self.run(["create databases {0};".format(database_name)])
        except Exception as e:
            pass
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

    def user_run(self, user_class, sequence: list, mechod='fetchone'):
        info_head = 'SQLManager ERR: '
        try:
            permission = cfg.database.permissions[user_class]
        except Exception as e:
            raise info_head + 'user_class not found'
        output = []
        cursor = self.conn.cursor()
        for item in sequence:
            for table in permission.keys():
                if table not in item:
                    continue
                permcode = permission.get(table, '')
                if 'w' in permcode:
                    pass
                elif 'r' in permcode:
                    if 'insert' in item or 'delete' in item or 'update' in item or 'create' in item or 'alter' in item:
                        raise info_head + \
                            "w {0} <{1}> no permission".format(
                                table, user_class)
                else:
                    raise info_head + \
                        "rw {0} <{1}> no permission".format(table, user_class)
            cursor.execute(item)
            self.conn.commit()
            if mechod == 'fetchone':
                output.append(str(cursor.fetchone()))
            elif mechod == 'fetchall':
                output.append(str(cursor.fetchall()))
        return output


if __name__ == '__main__':
    mng = SQLManager()
