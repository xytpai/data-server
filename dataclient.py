import socket
from crypto import *


if __name__ == '__main__':
    HOST = '0.0.0.0'
    PORT = 9999
    # recv pubkey_server
    rsa_client = RSAWrapper(True)
    rsa_server = RSAWrapper(False)
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.connect((HOST, PORT))
    rsa_server.load_pkcs1(sk.recv(10000).decode())
    # send pubkey
    sendmsg = 'hello' + rsa_client.get_pkcs1() + 'hi'
    sendsign = rsa_client.sign(sendmsg)
    sendmsg = ','.join([rsa_server.encrypt(sendmsg), sendsign])
    sk.send(sendmsg.encode())
    sk.close()
