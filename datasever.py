import ssl
import json
import random
import argparse
import asyncio
from datetime import datetime
from threading import Timer
import pymysql as sql


SQLINFO = {
    'host': 'localhost',
    'user': 'debian-sys-maint',
    'password': 'qqdWvUpyYdfW9crD'
}
KEYLEN = 100
ALPHABET = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ/=+'
user_cache = {}


def time_threading(inc):
    global user_cache
    user_cache = {}
    print(datetime.now(), 'update cache')
    t = Timer(inc, time_threading, (inc,))
    t.start()


time_threading(60*60*24*3)  # 3d


def process_sql(username, sql):
    outdata = {
        'status': 'ok'
    }
    return json.dumps(outdata)


def identify(username, password):
    conn = sql.connect(
        host=SQLINFO['host'],
        user=SQLINFO['user'],
        password=SQLINFO['password'],
        charset='utf8')
    cursor = conn.cursor()
    cursor.execute('use company;')
    conn.commit()
    cursor.execute(
        'select * from userpass where username=\"{0}\";'.format(username))
    conn.commit()
    datas = eval(str(cursor.fetchone()))
    exact_password = datas[1]
    conn.close()
    return password == exact_password


def process_main(recv):
    global user_cache
    method = recv['method']
    if method == 'login':
        username = recv['username']
        password = recv['password']
        if identify(username, password):
            key = ''
            for _ in range(KEYLEN):
                key += random.choice(ALPHABET)
            user_cache[username] = key
            resp = {'key': key, 'state': 'ok'}
            return json.dumps(resp)
        else:
            return None
    elif method == 'logout':
        username = recv['username']
        password = recv['password']
        if identify(username, password):
            user_cache.pop(username)
        else:
            return None
    elif method == 'sql':
        username = recv['username']
        key = recv['key']
        if user_cache.get(username, 'none') == 'none':
            return None
        elif user_cache[username] != key:
            return None
        return process_sql(username, recv['sql'])
    return None


async def handle_dataserver(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Connection {addr!r}")
    tab = '  '
    resp = None
    while True:
        try:
            recv = await reader.read(4096)
            recv = json.loads(recv.decode())
            print(tab + 'recv: ' + str(recv))
        except Exception as e:
            print(tab + 'Err in recv: ' + str(e))
            writer.close()
            return
        try:
            resp = process_main(recv)
        except:
            resp = None
        if resp is not None:
            try:
                writer.write(resp.encode())
                await writer.drain()
            except Exception as e:
                print(tab + 'error in send' + str(e))
                writer.close()
                return
        else:
            break
    print('End connection')
    writer.close()


async def run_server(host, port):
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.check_hostname = False
    ssl_context.load_cert_chain('openssl/server.crt', 'openssl/server.key')
    server = await asyncio.start_server(handle_dataserver, host, port, ssl=ssl_context)
    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Dataserver Demo')
    parser.add_argument('--host', default='0.0.0.0', type=str)
    parser.add_argument('--port', default='9999', type=str)
    args = parser.parse_args()
    asyncio.run(run_server(args.host, int(args.port)))
