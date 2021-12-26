import pymysql as sql


# def get_data():
#     conn = sql.connect(
#         host=info['host'],
#         user=info['user'],
#         password=info['password'],
#         charset='utf8')
#     cursor = conn.cursor()
#     cursor.execute("show databases;")
#     datas = cursor.fetchall()
#     datas =str(datas)
#     conn.close()
#     return datas
from flask import Flask, render_template, send_file
from flask_login import LoginManager
app = Flask(__name__)
app.secret_key = 'abc'
login = LoginManager()
login.init_app(app)
login.login_view = 'login'


@app.route('/<path:name>', methods=['GET'])
def get_path(name):
    return name

# @app.route('/', methods=['GET'])
# def get_index():
#     return get_data()

if __name__=='__main__':
	app.run(debug=True,host="0.0.0.0")