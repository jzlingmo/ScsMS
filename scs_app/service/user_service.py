# -*- coding: utf-8 -*-

import hashlib

from scs_app.db_connect import *
from scs_app.utils.time_format import now_timestamp


class UserService():
    def __init__(self):
        self.user_fields = '*'
        self.db = get_connection()

    def get_sid_by_username(self, username):
        rs = self.db.query('select sid from user where username =%s and visible=0', [username, ])
        return rs[0].get('sid')

    def get_user_by_sid(self, user_sid):
        sql = 'select ' + self.user_fields + ' from user where sid=%s and visible=0'
        params = [user_sid, ]
        user = self.db.get(sql, params)
        return user

    def get_user_by_username(self, username):
        sql = 'select ' + self.user_fields + ' from user where username=%s and visible=0'
        params = [username, ]
        user = self.db.get(sql, params)
        return user

    def get_user_by_username_and_password(self, username, password):
        sql = 'select ' + self.user_fields + ' from user where username=%s and password=%s and visible=0'
        password = hashlib.md5(password).hexdigest()
        params = [username, password]
        user = self.db.get(sql, params)
        return user

    def update_user_by_username(self, username, row_dict):
        where_dict = {'username': username}
        ps = row_dict.get('password')
        # 更新密码进行md5加密
        if ps:
            row_dict['password'] = hashlib.md5(row_dict.get('password')).hexdigest()

        # 信息更新时间戳
        row_dict['timestamp'] = now_timestamp()
        update_count = self.db.update_by_dict('user', row_dict, where_dict)
        return update_count
