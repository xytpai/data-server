import random
import rsa
from math import ceil
from base64 import b64encode, b64decode
from Crypto.Cipher import AES


class RSAWrapper:
    def __init__(self, keygen=True, keylength=1024) -> None:
        self.keylength = keylength
        self.chunk = keylength//8-11
        if keygen:
            pubkey, privkey = rsa.newkeys(keylength)
            self.pubkey = pubkey
            self.privkey = privkey

    def get_pkcs1(self) -> str:
        return str(self.pubkey.save_pkcs1(), 'utf-8')

    def load_pkcs1(self, pubkey) -> None:
        self.pubkey = rsa.PublicKey.load_pkcs1(pubkey)

    def encode(self, message) -> str:
        chunk = self.chunk
        divide = ceil(len(message)/float(chunk))
        cryptolalia = b''
        for i in range(divide):
            cryptolalia += rsa.encrypt(message[i *
                                               chunk:(i+1)*chunk].encode(), self.pubkey)
        return str(b64encode(cryptolalia), 'utf-8')

    def decode(self, cryptolalia) -> str:
        cryptolalia = b64decode(cryptolalia)
        chunk = self.keylength//8
        divide = len(cryptolalia)//chunk
        message = ''
        for i in range(divide):
            message += rsa.decrypt(cryptolalia[i *
                                               chunk:(i+1)*chunk], self.privkey).decode()
        return message

    def sign(self, message) -> str:
        signature = rsa.sign(message.encode(), self.privkey, 'SHA-256')
        return str(b64encode(signature), 'utf-8')

    def verify(self, message, signature):
        signature = b64decode(signature)
        return rsa.verify(message.encode(), signature, self.pubkey)


class AESWrapper:
    alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ/=+'

    def __init__(self, keygen=True, keylength=16) -> None:
        self.keylength = keylength
        if keygen:
            key = ''
            for _ in range(keylength):
                key += random.choice(self.alphabet)
            self.key = key
            self.cryptor = AES.new(key, AES.MODE_ECB)

    def get_key(self) -> str:
        return self.key

    def load_key(self, key) -> None:
        self.key = key
        self.keylength = len(key)
        self.cryptor = AES.new(key, AES.MODE_ECB)

    def encode(self, message) -> str:
        chunk = self.keylength
        divide = ceil(len(message)/float(chunk))
        r = len(message) % chunk
        message += '' if r == 0 else ' '*(chunk-r)
        cryptolalia = b''
        for i in range(divide):
            cryptolalia += self.cryptor.encrypt(
                message[i*chunk:(i+1)*chunk].encode())
        return str(b64encode(cryptolalia), 'utf-8')

    def decode(self, cryptolalia) -> str:
        cryptolalia = b64decode(cryptolalia)
        chunk = self.keylength
        divide = len(cryptolalia)//chunk
        message = ''
        for i in range(divide):
            message += self.cryptor.decrypt(
                cryptolalia[i*chunk:(i+1)*chunk]).decode()
        return message.rstrip()


if __name__ == '__main__':
    import time
    print('RSA Test', end='\n\n')
    myrsa = RSAWrapper()
    text = 'my rsa pubkey is\n' + myrsa.get_pkcs1()
    print('text:')
    print(text, end='\n\n')
    encode_start = time.time()
    cryptolalia = myrsa.encode(text)
    sign_start = time.time()
    signature = myrsa.sign(text)
    decode_start = time.time()
    decoded_text = myrsa.decode(cryptolalia)
    decode_end = time.time()
    print('cryptolalia:', sign_start-encode_start)
    print(cryptolalia, end='\n\n')
    print('signature:', decode_start-sign_start)
    print(signature, end='\n\n')
    print('decoded_text:', decode_end-decode_start)
    print(decoded_text, end='\n\n')
    myrsa.verify(decoded_text, signature)
    print('AES Test', end='\n\n')
    myaes = AESWrapper()
    encode_start = time.time()
    cryptolalia = myaes.encode(text)
    decode_start = time.time()
    decoded_text = myaes.decode(cryptolalia)
    decode_end = time.time()
    print('cryptolalia:', decode_start-encode_start)
    print(cryptolalia, end='\n\n')
    print('decoded_text:', decode_end-decode_start)
    print(decoded_text, end='\n\n')
