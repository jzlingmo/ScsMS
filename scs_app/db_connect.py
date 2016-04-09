__author__ = 'jz'

from flask import g

from common import torndb
# import torndb
from scs_app import config


def connect_db():
    database = torndb.Connection(host=config.HOST, database=config.DATABASE, user=config.USER, password=config.PASSWORD)
    return database


def get_connection():
    db = getattr(g, '_db', None)
    if db is None:
        db = g._db = connect_db()
    return db