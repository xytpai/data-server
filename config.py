from addict import Dict


cfg = Dict()

# database
cfg.database.host = 'localhost'
cfg.database.user = 'debian-sys-maint'
cfg.database.password = 'qqdWvUpyYdfW9crD'
cfg.database.base = 'company'
cfg.database.tables = {
    'userpass': 'username VARCHAR(20), password VARCHAR(256), class VARCHAR(20)',
    'userinfo': 'username VARCHAR(20), password VARCHAR(256), class VARCHAR(20)',
    'resource': 'username VARCHAR(20), password VARCHAR(256), class VARCHAR(20)',
}
cfg.database.permissions = {
    'admin': {
        'userpass': 'rw',
        'userinfo': 'rw',
        'resource': 'rw',
    },
    'guest': {
        'resource': 'r',
    },
}

# server
cfg.server.host = '192.168.0.106'
cfg.server.port = 9999
cfg.server.expiretime = 60*60*24*3

# random
cfg.alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ/=+'
cfg.tempkey_len = 128
