#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    @File        :models.py
    @Description :获取钉钉的access_token
    @DateTime    :2022-11-28 10:11
    @Author      :Jay Zhang
"""
import requests
from Db.database import redis
import config

CONFIG = config.get_settings()

DD_URL = CONFIG.dd_url
APP_KEY = CONFIG.dd_app_key
APP_SECRET = CONFIG.dd_app_secret


async def get_access_token() -> str:
    """
    获取本地存储的access_token

    :return: access_token
    """
    access_token = None
    try:
        access_token_key = 'dd_access_token'
        if redis.exists(access_token_key):
            access_token = str(redis.get(access_token_key))
        else:
            data = await http_get_access_token()
            if data and data['errcode'] == 0:
                redis.set(access_token_key, data['access_token'], ex=data['expires_in'])
                access_token = data['access_token']
        return access_token
    except Exception as er:
        raise er


async def http_get_access_token() -> dict:
    """
    通过钉钉接口获取access_token

    :return: json
    """
    url = f'{DD_URL}/gettoken'
    try:
        response = requests.get(url, params={'appkey': APP_KEY, 'appsecret': APP_SECRET})
        if response.status_code == 200:
            print(response.json())
            return response.json()
    except Exception as e:
        raise e
