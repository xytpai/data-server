from config import cfg
import socket
import json
import ssl


if __name__ == '__main__':
    host = cfg.server.host
    port = cfg.server.port
    ssl_context = ssl.create_default_context()
    ssl_context.load_verify_locations('openssl/ca.crt')
    with socket.create_connection((host, port)) as sock:
        with ssl_context.wrap_socket(sock, server_hostname=host) as ssock:
            data = {
                'method': 'login',
                'username': 'root',
                'password': 'mypassword'
            }
            ssock.send(json.dumps(data).encode())
            recv = json.loads(ssock.recv(10000).decode())
            print(recv)
            # data = {
            #     'method': 'sql',
            #     'username': 'asd',
            #     'key': 'N0QPozmF0xIAfPbhPC+mWLet2xKyCx9pVc+ne38L8HzXeMZLLzD1K+xN4Luf0/5xm+CzprSXUdO/iIGEyEJ9STwlLTiJR43M/se4',
            #     'sql': 'asdasd'
            # }
            # ssock.send(json.dumps(data).encode())
            # recv = ssock.recv(10000).decode()
            # print(recv)

    # ssl_context.check_hostname = False
    # ssl_context.load_cert_chain('ca.crt', 'privkey.pem')
    # sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sk.connect((HOST, PORT))
    # with ssl_context.wrap_socket(sk, server_hostname='127.0.0.1') as ssk:
    #     data = {
    #         'method': 'get_pubkey',
    #     }
    #     ssk.send(json.dumps(data).encode())
    #     recv = ssk.recv(100).decode()
    #     # recv = json.loads(sk.recv(10000).decode())
    #     print(recv)
    #     ssk.close()
