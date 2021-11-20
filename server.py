import pymysql as sql

host = 'localhost'
user = 'debian-sys-maint'
password = 'qqdWvUpyYdfW9crD'

conn = sql.connect(
    host=host,
    user=user,
    password=password,
    charset='utf8')
cursor = conn.cursor()
cursor.execute("show databases;")
print(cursor.fetchall())
cursor.execute("show databases;")
print(cursor.fetchall())
conn.close()