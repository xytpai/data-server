import asyncio
from crypto import *
from sqlbase import *


def split_rsa_data(message):
    rsa_start = '-----BEGIN RSA PUBLIC KEY-----'
    rsa_end = '-----END RSA PUBLIC KEY-----'
    head = message[:message.find(rsa_start)]
    tail = message[message.find(rsa_end) + len(rsa_end):]
    rsadata = message[len(head):-len(tail)]
    return head, rsadata, tail


def process_first_contact(head, tail):
    print(head)
    print(tail)


def process_command(cmd):
    cmd = cmd.strip().split(' ')
    cmd = [t for t in cmd if len(t) > 0]
    if cmd[0] == 'login':
        return 'process login'
    return None


async def handle_dataserver(reader, writer):
    # send pubkey
    try:
        rsa_server = RSAWrapper(True)
        writer.write(rsa_server.get_pkcs1().encode())
        await writer.drain()
    except Exception as e:
        print('faild to send pubkey')
        writer.close()
        return
    # recv pubkey_client, head and tail
    try:
        rsa_clien = RSAWrapper(False)
        recvmsg = await reader.read(4096)
        recvmsg = recvmsg.decode()
        recvmsg, recvsign = recvmsg.split(',')
        recvmsg = rsa_server.decrypt(recvmsg)
        head, pubkey_client, tail = split_rsa_data(recvmsg)
        rsa_clien.load_pkcs1(pubkey_client)
        rsa_clien.verify(recvmsg, recvsign)
        process_first_contact(head.strip(), tail.strip())
        addr = writer.get_extra_info('peername')
        print(f"Received {recvmsg!r} from {addr!r}")
    except Exception as e:
        print('faild to recv pubkey_client')
        writer.close()
        return
    # send aes key
    # response = process_command(recvmsg)
    # while response is not None:
    #     try:
    #         response = rsa.encrypt(response.encode(), pubkey_client)
    #         response = str(base64.b64encode(response), 'utf-8')
    #         writer.write(response.encode())
    #         await writer.drain()
    #     except Exception as e:
    #         print('faild to send message')
    #         writer.close()
    #         return
    #     try:
    #         data = await reader.read(10000)
    #         message = data.decode()
    #         message = base64.b64decode(message)
    #         message = rsa.decrypt(message, privkey).decode()
    #         print(f"Received {message!r} from {addr!r}")
    #     except Exception as e:
    #         print('faild to get message')
    #         writer.close()
    #         return
    #     response = process_command(message)
    # writer.close()


async def run_server(host, port):
    server = await asyncio.start_server(handle_dataserver, host, port)
    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    HOST = '0.0.0.0'
    PORT = 9999
    asyncio.run(run_server(HOST, PORT))
