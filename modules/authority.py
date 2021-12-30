import random


class AuthorityManager:
    def __init__(self, sql_manager) -> None:
        self.sql_manager = sql_manager
        self.cfg = sql_manager.cfg

    def authorize(self, username, command) -> bool:
        return True
