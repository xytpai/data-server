import json
import socket
import ssl
from config import cfg

host = cfg.server.host
port = cfg.server.port

ssl_context = ssl.create_default_context()
ssl_context.load_verify_locations('openssl/ca.crt')
with socket.create_connection((host, port)) as sock:
    with ssl_context.wrap_socket(sock, server_hostname=host) as ssock:
        while True:
            method = input('please enter <method>: ')
            resp = 'invalid method'
            if method == 'exit':
                break
            elif method == 'login':
                info = input('please enter <username, password>: ')
                info = info.split(',')
                username = info[0].strip()
                password = info[1].strip()
                resp = {'method': method,
                        'username': username, 'password': password}
                ssock.send(json.dumps(resp).encode())
                resp = json.loads(ssock.recv(10000).decode())
            elif method == 'logout':
                info = input('please enter <username, key>: ')
                info = info.split(',')
                username = info[0].strip()
                key = info[1].strip()
                resp = {'method': method, 'username': username, 'key': key}
                ssock.send(json.dumps(resp).encode())
                resp = json.loads(ssock.recv(10000).decode())
            elif method == 'sql':
                info = input('please enter <username, key, sql>: ')
                info = info.split(',')
                username = info[0].strip()
                key = info[1].strip()
                sql = ",".join(info[2:])
                resp = {'method': method, 'username': username,
                        'key': key, 'sql': sql}
                ssock.send(json.dumps(resp).encode())
                resp = json.loads(ssock.recv(10000).decode())
            print(resp)
