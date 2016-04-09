# -*- coding: utf-8 -*-
__author__ = 'jz'

from flask.ext import restful
from flask.ext.restful import reqparse

from scs_app.db_connect import *
from scs_app.service.user_service import UserService
from scs_app.service.session_service import SessionService

parser = reqparse.RequestParser()
# 用于解析请求中的参数至指定类型 不存在该参数则值为None
parser.add_argument('username', type=str)
parser.add_argument('password', type=str)
parser.add_argument('api_key', type=str)

# 登录接口（权限） 根据用户名和密码创建session 根据sessionid删除session
class SessionResource(restful.Resource):
    def __init__(self):
        self.db = get_connection()
        self.user_service = UserService()
        self.session_service = SessionService()

    # 创建session 返回token
    def post(self):
        args = parser.parse_args()
        username = args.get('username', '')
        password = args.get('password', '')
        result = {'api_key': '', 'user': ''}
        # 查询用户是否存在
        user = self.user_service.get_user_by_username_and_password(username, password)
        if not user:
            return [], 404

        # 生成api_key返回
        result['api_key'] = self.session_service.create_session(username, password)
        result['user'] = user
        return result

    # 删除session
    def delete(self):
        args = parser.parse_args()
        api_key = args.get('api_key', '')

        self.session_service.delete_session(api_key)
        username = self.session_service.get_username_from_api_key(api_key)
        return 'log out ' + username
