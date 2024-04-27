from enum import Enum


class Permission(str, Enum):
    READ = 100
    WRITE = 200
    ONLYSEE = 300
