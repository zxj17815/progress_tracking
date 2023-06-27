#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    @File        :user_info.py
    @Description :
    @DateTime    :2023-06-16 10:16
    @Author      :Jay Zhang
"""
import json
from typing import List

import requests
import config
from fastapi import APIRouter, Depends, HTTPException, Query

from Permission.models import Permission
from Permission.schemas import PermissionBase, UserPermissionList
from User.models import User
from User.schemas import UserInfo
from Utils import access
from Db.database import SessionLocal

CONFIG = config.get_settings()

DD_URL = CONFIG.dd_url
DD_APP_KEY = CONFIG.dd_app_key
DD_APP_SECRET = CONFIG.dd_app_secret

DEPT = {
    '575251037': '制一车间',
    '575696026': '制二车间',
    '575261041': '制三车间',
    '575704034': '制四车间',
    # '574924074': '信息部-测试'
}

router = APIRouter(prefix="/users")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @router.get("/user_by_auth_code", response_model=UserInfo)
async def get_user_by_auth_code(code: str):
    try:
        data = {
            "clientId": DD_APP_KEY,
            "clientSecret": "-OXdAz_mbrfXJbzhhKQGYt0_T1dwJW-Smm6FXudgUnsqw7i7U8XwEesRYynP35ic",
            "code": code,
            "grantType": "authorization_code"
        }
        header = {
            "Content-Type": "application/json"
        }
        user_access_token_data = requests.post(f'https://api.dingtalk.com/v1.0/oauth2/userAccessToken',
                                               data=json.dumps(data), headers=header).json()
        if user_access_token_data and 'accessToken' in user_access_token_data:
            union_id_data = requests.get(f'https://api.dingtalk.com/v1.0/contact/users/me', headers={
                "x-acs-dingtalk-access-token": user_access_token_data['accessToken']
            }).json()
            if union_id_data and 'unionId' in union_id_data:
                user_id_data = requests.get(f'{DD_URL}/user/getUseridByUnionid', params={
                    "access_token": await access.get_access_token(),
                    "unionid": union_id_data['unionId']
                }).json()
                if user_id_data and 'userid' in user_id_data:
                    user_info_data = requests.get(f'{DD_URL}/user/get', params={
                        "access_token": await access.get_access_token(),
                        "userid": user_id_data['userid']
                    }).json()
                    if user_info_data and 'name' in user_info_data:
                        user_info = UserInfo(user_id=user_id_data['userid'])
                        user_info.employee_name = user_info_data['name']
                        if 'jobnumber' in user_info_data:
                            user_info.employee_id = user_info_data['jobnumber']
                        else:
                            user_info.employee_id = ""
                        return user_info
                    else:
                        raise HTTPException(status_code=400, detail="获取用户信息失败")
                else:
                    raise HTTPException(status_code=400, detail="获取用户信息失败")
            else:
                raise HTTPException(status_code=400, detail="获取用户信息失败")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="获取用户信息失败")


async def get_user_id_by_code(code: str) -> str:
    """
    通过code获取用户id

    :param code:免登录code
    :return: user_id
    """
    access_token = await access.get_access_token()
    data = requests.post(f'{DD_URL}/topapi/v2/user/getuserinfo',
                         data={"code": code},
                         params={"access_token": access_token}).json()
    if data and data['errcode'] == 0:
        return data['result']['userid']
    else:
        return ""


@router.get("/user_by_code", response_model=UserInfo)
async def get_user_by_code(code: str, db: SessionLocal = Depends(get_db)) -> UserInfo:
    """
    通过用户免登code获取数据

    :param db:
    :param code:免登录code
    :return: 用户信息json
    """
    access_token = await access.get_access_token()
    user_id = await get_user_id_by_code(code)
    user_info = UserInfo(user_id=user_id)
    data = requests.post(f'{DD_URL}/topapi/v2/user/get',
                         data={"userid": user_id},
                         params={"access_token": access_token}).json()
    if data and data['errcode'] == 0:
        user_info.employee_name = data['result']['name']
        for d in data['result']['dept_id_list']:
            if d in DEPT:
                user_info.dept_name = DEPT[d]
                break
        if 'job_number' in data['result']:
            user_info.employee_id = data['result']['job_number']
        else:
            user_info.employee_id = "钉钉暂无工号"
    return user_info


@router.get("/user_permission", response_model=UserPermissionList)
async def get_user_permission(db: SessionLocal = Depends(get_db),
                              employee_id: str = Query(..., min_length=1, max_length=20)):
    """
    获取用户权限

    :param db:

    :param employee_id:

    :return: 用户权限列表
    """
    user = db.query(User).filter(User.employee_id == employee_id).first()
    if user:
        return {"employee_id": employee_id, "permission": user.permission}
    else:
        raise HTTPException(status_code=400, detail=[
            {
                "loc": [
                    "body",
                    "employee_id"
                ],
                "msg": "user is not exist",
                "type": "value_error.missing"
            }
        ])


@router.post("/user_permission", response_model=UserPermissionList)
async def add_user_permission(db: SessionLocal = Depends(get_db),
                              employee_id: str = Query(..., min_length=1, max_length=20),
                              permission_id: int = Query(..., ge=0, le=15)):
    """
    添加某个用户的权限

    :param db:

    :param employee_id:

    :param permission_id:

    :return: 用户权限列表
    """
    user = db.query(User).filter(User.employee_id == employee_id).first()
    permission_obj = db.query(Permission).filter(Permission.id == permission_id).first()
    if not permission_obj:
        raise HTTPException(status_code=400, detail=[
            {
                "loc": [
                    "body",
                    "permission"
                ],
                "msg": "permission is not exist",
                "type": "value_error.missing"
            }
        ])
    if user:
        permission_list = [item.id for item in user.permission]
        if permission_id not in permission_list:
            user.permission.append(permission_obj)
            db.commit()
            db.refresh(user)
        return {"employee_id": employee_id, "permission": user.permission}
    else:
        raise HTTPException(status_code=400, detail=[
            {
                "loc": [
                    "body",
                    "employee_id"
                ],
                "msg": "user is not exist",
                "type": "value_error.missing"
            }
        ])


@router.delete("/user_permission", response_model=UserPermissionList)
async def delete_user_permission(db: SessionLocal = Depends(get_db),
                                 employee_id: str = Query(..., min_length=1, max_length=20),
                                 permission_id: int = Query(..., ge=0, le=15)):
    """
    删除某个用户的权限

    :param db:

    :param employee_id:

    :param permission_id:

    :return: 用户权限列表
    """
    user = db.query(User).filter(User.employee_id == employee_id).first()
    permission_obj = db.query(Permission).filter(Permission.id == permission_id).first()
    if not permission_obj:
        raise HTTPException(status_code=400, detail=[
            {
                "loc": [
                    "body",
                    "permission"
                ],
                "msg": "permission is not exist",
                "type": "value_error.missing"
            }
        ])
    if user:
        permission_list = [item.id for item in user.permission]
        if permission_id not in permission_list:
            user.permission.pop(permission_obj)
            db.commit()
            db.refresh(user)
        return {"employee_id": employee_id, "permission": user.permission}
    else:
        raise HTTPException(status_code=400, detail=[
            {
                "loc": [
                    "body",
                    "employee_id"
                ],
                "msg": "user is not exist",
                "type": "value_error.missing"
            }
        ])
