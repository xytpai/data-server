import os
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
            if os.path.exists('pubkey.pem') and os.path.exists('privkey.pem'):
                with open('pubkey.pem', 'rb') as f:
                    self.pubkey = rsa.PublicKey.load_pkcs1(f.read())
                with open('privkey.pem', 'rb') as f:
                    self.privkey = rsa.PrivateKey.load_pkcs1(f.read())
            else:
                pubkey, privkey = rsa.newkeys(keylength)
                with open('pubkey.pem', 'wb') as f:
                    f.write(pubkey.save_pkcs1())
                with open('privkey.pem', 'wb') as f:
                    f.write(privkey.save_pkcs1())
                self.pubkey = pubkey
                self.privkey = privkey

    def get_pkcs1(self) -> str:
        return str(self.pubkey.save_pkcs1(), 'utf-8')

    def load_pubkey(self, pubkey) -> None:
        self.pubkey = rsa.PublicKey.load_pkcs1(pubkey)

    def encrypt(self, message) -> str:
        chunk = self.chunk
        divide = ceil(len(message)/float(chunk))
        cryptolalia = b''
        for i in range(divide):
            cryptolalia += rsa.encrypt(message[i *
                                               chunk:(i+1)*chunk].encode(), self.pubkey)
        return str(b64encode(cryptolalia), 'utf-8')

    def decrypt(self, cryptolalia) -> str:
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

    def encrypt(self, message) -> str:
        chunk = self.keylength
        divide = ceil(len(message)/float(chunk))
        r = len(message) % chunk
        message += '' if r == 0 else ' '*(chunk-r)
        cryptolalia = b''
        for i in range(divide):
            cryptolalia += self.cryptor.encrypt(
                message[i*chunk:(i+1)*chunk].encode())
        return str(b64encode(cryptolalia), 'utf-8')

    def decrypt(self, cryptolalia) -> str:
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
    encrypt_start = time.time()
    cryptolalia = myrsa.encrypt(text)
    sign_start = time.time()
    signature = myrsa.sign(text)
    decrypt_start = time.time()
    decrypt_text = myrsa.decrypt(cryptolalia)
    decrypt_end = time.time()
    print('cryptolalia:', sign_start-encrypt_start)
    print(cryptolalia, end='\n\n')
    print('signature:', decrypt_start-sign_start)
    print(signature, end='\n\n')
    print('decrypt_text:', decrypt_end-decrypt_start)
    print(decrypt_text, end='\n\n')
    myrsa.verify(decrypt_text, signature)
    print('AES Test', end='\n\n')
    myaes = AESWrapper()
    encrypt_start = time.time()
    cryptolalia = myaes.encrypt(text)
    decrypt_start = time.time()
    decrypt_text = myaes.decrypt(cryptolalia)
    decrypt_end = time.time()
    print('cryptolalia:', decrypt_start-encrypt_start)
    print(cryptolalia, end='\n\n')
    print('decrypt_text:', decrypt_end-decrypt_start)
    print(decrypt_text, end='\n\n')
