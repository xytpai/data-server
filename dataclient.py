import socket
import json
import ssl


if __name__ == '__main__':
    HOST = '0.0.0.0'
    PORT = 9999
    # ssl_context = ssl._create_unverified_context()
    ssl_context = ssl.create_default_context()
    # ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.load_verify_locations('ca.crt')
    with socket.create_connection((HOST, PORT)) as sock:
        with ssl_context.wrap_socket(sock, server_hostname=HOST) as ssock:
            print(ssock.version())

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
