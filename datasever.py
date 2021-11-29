import asyncio
import json
import ssl
from collections import defaultdict
from sqlbase import *


user_cache = defaultdict(dict)


# def login(username, password, pubkey_client):
#     print('processing login:', username, password)
#     rsa_client = RSAWrapper(False)
#     rsa_client.load_pubkey(pubkey_client)
#     aes = AESWrapper(True)
#     user_cache[username] = {'rsa': rsa_client, 'aes': aes}
#     resp = {'key': rsa_client.encrypt(aes.get_key())}
#     return json.dumps(resp)


# def logout(username):
#     print('processing logout:', username)
#     if len(user_cache[username]) == 0:
#         return None
#     aes = user_cache[username]['aes']
#     user_cache[username] = {}
#     return None


def process_main(recv):
    method = recv['method']
    if method == 'get_pubkey':
        resp = {'pubkey': 'hello'}
        return json.dumps(resp)
    # elif method == 'login':
    #     pubkey_client = rsa_server.decrypt(recv['pubkey'])
    #     username = rsa_server.decrypt(recv['username'])
    #     password = rsa_server.decrypt(recv['password'])
    #     return login(username, password, pubkey_client)
    # elif method == 'logout':
    #     username = recv['username']
    #     key = recv['key']
    #     return logout(username, key)
    # elif method == 'echo':
    #     username = recv['username']
    #     if len(user_cache[username]) == 0:
    #         return None
    #     aes = user_cache[username]['aes']
    #     key = aes.decrypt(recv['key'])
    #     if key != aes.get_key():
    #         return None
    #     data = 'echo: ' + aes.decrypt(recv['data'])
    #     resp = {'data': aes.encrypt(data)}
    #     return json.dumps(resp)


async def handle_dataserver(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Connection {addr!r}")
    resp = 'start'
    while True:
        try:
            recv = await reader.read(4096)
            recv = json.loads(recv.decode())
            print(recv)
        except Exception as e:
            print('error in recv')
            writer.close()
            return
        resp = process_main(recv)
        if resp is not None:
            try:
                writer.write(resp.encode())
                await writer.drain()
            except Exception as e:
                print('error in send')
                writer.close()
                return
        else:
            break
    writer.close()


async def run_server(host, port):
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.check_hostname = False
    ssl_context.load_cert_chain('server.crt', 'server.key')
    server = await asyncio.start_server(handle_dataserver, host, port, ssl=ssl_context)
    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    HOST = '0.0.0.0'
    PORT = 9999
    asyncio.run(run_server(HOST, PORT))
