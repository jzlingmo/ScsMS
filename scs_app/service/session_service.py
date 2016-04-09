# -*- coding: utf-8 -*-

import string
import base64

from scs_app.db_connect import get_connection
from scs_app.utils.time_format import now_timestamp

api_key_dict = {}


class SessionService():
    def __init__(self):
        self.db = get_connection()

    def create_session(self, username,password):
        # 简单加密api_key
        session_string = '|'.join((username, password))
        session_id = base64.b64encode(session_string)
        api_key_dict[session_id] = now_timestamp()
        # self.db.insert("insert into session(k,v) values (%s,%s)", (session_id, now_timestamp())) # use db
        return session_id

    def get_username_from_api_key(self, api_key):
        if not api_key:
            return None
        session_string = base64.b64decode(api_key)
        username = string.split(session_string, '|')[0]
        return username

    def validate_api_key(self, api_key):
        rs = api_key_dict.get(api_key)
        # rs = self.db.get("select * from session where k=%s", (api_key,))
        if rs:
            return True
        return False

    def delete_session(self, api_key):
        # self.db.execute("delete from session where k=%s", (api_key,))
        if api_key_dict.get(api_key):
            del api_key_dict[api_key]

    def update_session(self, api_key):
        # self.db.update("update session set v=%s where k=%s", (now_timestamp(), api_key))
        api_key_dict[api_key] = now_timestamp()