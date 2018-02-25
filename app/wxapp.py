# -*- coding: UTF-8 -*-
from weixin.oauth2 import OAuth2AuthExchangeError
from weixin.lib.wxcrypt import WXBizDataCrypt
from models import UserWX as UserWXModel
from models import User as UserModel
from datetime import datetime
from weixin import WXAPPAPI
from flask import abort
from app import db
import time
import jwt

def get_wxapp_userinfo(encrypted_data, iv, code):
    appid = 'wx4570344745a0bdc8'
    secret = 'cab82f01992be971923d56c3b0f86d45'
    api = WXAPPAPI(appid=appid, app_secret=secret)
    try:
        session_info = api.exchange_code_for_session_key(code=code)
    except OAuth2AuthExchangeError as e:
        # raise Unauthorized(e.code, e.description)
        abort(401)
    session_key = session_info.get('session_key')
    crypt = WXBizDataCrypt(appid, session_key)
    user_info = crypt.decrypt(encrypted_data, iv)
    return user_info, session_key


def verify_wxapp(encrypted_data, iv, code):
    user_info, session_key = get_wxapp_userinfo(encrypted_data, iv, code)
    openid = user_info.get('openId', None)
    if openid:
        user = UserModel.query.filter_by(id=openid).first()
        if not user:
            sql_body = UserModel(id=user_info['openId'], nickname=user_info['nickName'], 
                    province=user_info['province'],country=user_info['country'],
                    city=user_info['city'],gender=user_info['gender'],
                    created_time=datetime.now(), updated_time=datetime.now())
            db.session.add(sql_body)
            db.session.commit()
    return user_info, session_key

def create_token(request):
    # verify basic token
    approach = request.get('auth_approach')
    username = request['username']
    password = request['password']
    
    if approach == 'wxapp':
        account, session_key = verify_wxapp(username, password, request.get('code'))
    if not account:
        return False, {}
    payload = {
        "iss": 'wxapp',
        "iat": int(time.time()),
        "exp": int(time.time()) + 86400 * 7,
        "aud": 'flask',
        "sub": str(account['openId']),
        "nickname": account['nickName'],
        "scopes": ['open']
    }
    token = jwt.encode(payload, 'secret', algorithm='HS256')
    # save token openid session_key
    sql_body = UserWXModel(id=token, openid=account['openId'],
                    session_key=session_key,created_time=datetime.now(),
                    updated_time=datetime.now())
    db.session.add(sql_body)
    db.session.commit()

    return True, {'access_token': token,
                  'nickname': account['nickName'],
                  'openid': str(account['openId']),
                  'avatarUrl':account['avatarUrl']}
