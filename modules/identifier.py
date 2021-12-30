import json
import random
from datetime import datetime
from threading import Timer


class Identifier:
    def __init__(self, sql_manager, tempkey_len=128) -> None:
        self.sql_manager = sql_manager
        self.cfg = sql_manager.cfg
        self.user_key_cache = {}
        self.tempkey_len = tempkey_len
        self.alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ/=+'

        def time_threading(inc):
            self.user_key_cache = {}
            print(datetime.now(), 'update cache')
            t = Timer(inc, time_threading, (inc,))
            t.start()
        time_threading(self.cfg.server.expiretime)

    def login(self, username, password) -> str:
        if self.__identify(username, password):
            key = ''
            for _ in range(self.tempkey_len):
                key += random.choice(self.alphabet)
            self.user_key_cache[username] = key
            resp = {'key': key, 'state': 'ok'}
        else:
            resp = {'state': 'denied'}
        return json.dumps(resp)

    def logout(self, username, password) -> str:
        if self.__identify(username, password):
            self.user_key_cache.pop(username)
            resp = {'state': 'ok'}
        else:
            resp = {'state': 'denied'}
        return json.dumps(resp)

    def run(self, username, key, function, command) -> str:
        if self.user_key_cache.get(username, 'none') == 'none':
            resp = {'state': 'denied'}
        elif self.user_key_cache[username] != key:
            resp = {'state': 'denied'}
        else:
            resp = function(username, command)
        return json.dumps(resp)

    def __identify(self, username, password) -> bool:
        global sql_manager
        output = self.sql_manager.run(
            ['select salt, password from {0} where id=\"{1}\";'.format('user', username)], mechod='fetchone')
        output = eval(output[-1])
        salt = output[0]
        exact_password = output[1]
        password = self.cfg.function.encode_password(password, salt)
        return password == exact_password
