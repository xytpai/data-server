import ssl
import json
import random
import asyncio
import modules
from config import cfg


sql_manager = modules.SQLManager(cfg)
auth_manager = modules.AuthorityManager(sql_manager)
identifier = modules.Identifier(sql_manager)


def process_sql(username, sql) -> str:
    if auth_manager.authorize(username, sql):
        try:
            output = sql_manager.run([sql])
            resp = {'state': 'ok', 'info': str(output[0])}
        except Exception as e:
            resp = {'state': 'error', 'info': str(e)}
    else:
        resp = {'state': 'denied'}
    return resp


def process_main(recv):
    global user_key_cache
    method = recv['method']
    if method == 'login':
        return identifier.login(recv['username'], recv['password'])
    elif method == 'logout':
        return identifier.logout(recv['username'], recv['password'])
    elif method == 'sql':
        return identifier.run(recv['username'], recv['key'], process_sql, recv['sql'])
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
