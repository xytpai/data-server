from addict import Dict


cfg = Dict()

# database
cfg.database.host = 'localhost'
cfg.database.user = 'debian-sys-maint'  # modify it
cfg.database.password = 'qqdWvUpyYdfW9crD'  # modify it
cfg.database.base = 'company'
cfg.database.tables = {
    'user': [
        'id bigint auto_increment primary key',
        'username varchar(36) not null unique',
        'salt varchar(64) not null',
        'password varchar(128) not null',  # md5(sha1(pwd) + salt)
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
        'id bigint auto_increment primary key',
        'parent_id bigint default null',
        'name varchar(255) not null unique',
        'code varchar(255) not null',
        'intro varchar(255) default null',
    ],
    'role': [
        'id bigint auto_increment primary key',
        'parent_id bigint default null',
        'name varchar(255) not null unique',
        'intro varchar(255) default null',
    ],
    'user_role': [
        'user_id bigint not null',
        'role_id bigint not null',
        'primary key(user_id, role_id)',
    ],
    'role_permission': [
        'role_id bigint not null',
        'permission_id bigint not null',
        'primary key(role_id, permission_id)',
    ],
    'resource': [
        'id bigint auto_increment primary key',
        'username varchar(36) not null unique',
        'count bigint'
    ],
}

# init
cfg.database.init = {
    'user': [[None, 'root', 'qwe', 'pwd', 'root', None, None, None, None, None, None, None, None]],
    'permission': [[None, None, 'sudo', 'rw all', 'overall']],
    'role': [[None, None, 'admin', 'rwall', 'no limit']],
    'user_role': [[0, 0]],
    'role_permission': [[0, 0]]
}

# server
cfg.server.host = '192.168.0.106'
cfg.server.port = 9999
cfg.server.expiretime = 60*60*24*3

# random
cfg.alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ/=+'
cfg.tempkey_len = 128
