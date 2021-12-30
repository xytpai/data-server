import ssl
import json
import random
import asyncio
from datetime import datetime
from threading import Timer
from sqlmanager import *
from config import cfg


sql_manager = SQLManager()
auth_manager = AuthorityManager(sql_manager)
user_key_cache = {}


def time_threading(inc):
    global user_key_cache
    user_key_cache = {}
    print(datetime.now(), 'update cache')
    t = Timer(inc, time_threading, (inc,))
    t.start()


time_threading(cfg.server.expiretime)


def process_sql(username, sql):
    state_ok = {
        'state': 'ok'
    }
    state_error = {
        'state': 'error'
    }
    state_denied = {
        'state': 'denied'
    }
    if auth_manager.authorize(username, sql):
        try:
            output = sql_manager.run([sql])
            state_ok['info'] = str(output[0])
            return json.dumps(state_ok)
        except Exception as e:
            state_error['info'] = str(e)
            return json.dumps(state_error)
    else:
        return json.dumps(state_denied)


def identify(username, password, table_name='user'):
    global sql_manager
    output = sql_manager.run(
        ['select salt, password from {0} where id=\"{1}\";'.format(table_name, username)], mechod='fetchone')
    output = eval(output[-1])
    salt = output[0]
    exact_password = output[1]
    password = cfg.function.encode_password(password, salt)
    return password == exact_password


def process_main(recv):
    global user_key_cache
    method = recv['method']
    if method == 'login':
        username = recv['username']
        password = recv['password']
        if identify(username, password):
            key = ''
            for _ in range(cfg.tempkey_len):
                key += random.choice(cfg.alphabet)
            user_key_cache[username] = key
            resp = {'key': key, 'state': 'ok'}
            return json.dumps(resp)
        else:
            return None
    elif method == 'logout':
        username = recv['username']
        password = recv['password']
        if identify(username, password):
            user_key_cache.pop(username)
        else:
            return None
    elif method == 'sql':
        username = recv['username']
        key = recv['key']
        if user_key_cache.get(username, 'none') == 'none':
            return None
        elif user_key_cache[username] != key:
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
    asyncio.run(run_server(cfg.server.host, cfg.server.port))
