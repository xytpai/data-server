import pymysql as sql

sql_info = {
    'host' : 'localhost',
    'user' : 'debian-sys-maint',
    'password' : 'qqdWvUpyYdfW9crD'
}

def login(username, password):
    conn = sql.connect(
        host=sql_info['host'],
        user=sql_info['user'],
        password=sql_info['password'],
        charset='utf8')
    cursor = conn.cursor()
    cursor.execute("show databases;")
    datas = cursor.fetchall()
    datas =str(datas)
    conn.close()
    return datas
