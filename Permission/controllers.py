#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    @File        :controllers.py
    @Description :
    @DateTime    :2023/6/27 4:48 PM
    @Author      :Jay Zhang
"""
from typing import List

from fastapi import APIRouter, Depends

from Db.database import SessionLocal
from Permission.models import Permission
from Permission.schemas import PermissionList

router = APIRouter(prefix="/permissions")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/all", response_model=List[PermissionList])
async def get_all_permissions(db=Depends(get_db)):
    """
    获取所有权限


    :param db:
    :return:
    """
    return db.query(Permission).all()
