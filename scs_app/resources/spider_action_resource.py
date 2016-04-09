# -*- coding: utf-8 -*-
__author__ = 'jz'

import os
import subprocess

from flask.ext import restful
from flask.ext.restful import reqparse

from scs_app.db_connect import *

parser = reqparse.RequestParser()

parser.add_argument('sid', type=str)


class SpiderActionResource(restful.Resource):
    def __init__(self):
        self.db = get_connection()

    def post(self, action):
        args = parser.parse_args()
        if action == 'start':
            rs = self.db.get('select sid,script from spider limit 0,1')
            sid = rs['sid']
            script = rs['script']
            process = subprocess.Popen('python %s' % script)
            pid = process.pid
            self.db.update_by_dict('spider', {'pid': pid}, {'sid': sid})
            return pid
        elif action == 'stop':
            sid = args.get('sid')
            if not sid:
                return 'spider not running', 404
            pid = self.db.get('select pid from spider where sid=%s' % sid)['pid']
            os.kill(int(pid), 9)
            self.db.update_by_dict('spider', {'pid': None}, {'sid': sid})
            return 'stop success'
        else:
            return 'action not support', 404