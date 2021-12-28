from addict import Dict
import hashlib
cfg = Dict()


def encode_password(password, salt):
    s1 = hashlib.sha1()
    s256 = hashlib.sha256()
    s1.update(password.encode())
    s256.update((s1.hexdigest() + salt).encode())
    return s256.hexdigest()


# function
cfg.function.encode_password = encode_password


# database
cfg.database.host = 'localhost'
cfg.database.user = 'debian-sys-maint'  # modify it
cfg.database.password = 'qqdWvUpyYdfW9crD'  # modify it
cfg.database.base = 'company'
cfg.database.tables = {
    'user': [
        'id varchar(36) primary key',
        'salt varchar(64) not null',
        'password varchar(64) not null',  # sha256(sha1(pwd) + salt)
        'name varchar(255) default null',
        'mobile varchar(15) default null',
        'state tinyint default 1',  # 1:enable, 0:disable
        'deleted tinyint default 0',  # 1:deleted, 0:normal
        'created date default null',
        'edited date default null',
        'creator varchar(36) default null',
        'editor varchar(36) default null',
    ],
    'permission': [
        'id varchar(36) primary key',
        'parent_id varchar(36) default null',
        'intro varchar(255) default null',
        'code varchar(255) not null',
    ],
    'role': [
        'id varchar(36) primary key',
        'parent_id varchar(36) default null',
        'intro varchar(255) default null',
    ],
    'user_role': [
        'user_id varchar(36) not null',
        'role_id varchar(36) not null',
        'primary key(user_id, role_id)',
    ],
    'role_permission': [
        'role_id varchar(36) not null',
        'permission_id varchar(36) not null',
        'primary key(role_id, permission_id)',
    ],
    'resource': [
        'name varchar(36) primary key',
        'count bigint'
    ],
}
cfg.database.init = {
    'user': [['root', 'rsalt', cfg.function.encode_password(cfg.database.password, 'rsalt'), None, None, None, None, None, None, None, None]],
    'permission': [['sudo', None, 'no limit', 'sudo']],
    'role': [['admin', None, 'use sudo permission']],
    'user_role': [['root', 'admin']],
    'role_permission': [['admin', 'sudo']]
}


# server
cfg.server.host = '192.168.0.106'
cfg.server.port = 9999
cfg.server.expiretime = 60*60*24*3


# random
cfg.alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ/=+'
cfg.tempkey_len = 128
