#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    @File        :api_version_router.py
    @Description :api版本路由
    @DateTime    :2023/6/29 11:17 AM
    @Author      :Jay Zhang
"""
from fastapi import APIRouter
from Tracking.controllers import router as tracking_router
from User.controllers import router as user_router
from Permission.controllers import router as permission_router

# 初始API版本路由
router = APIRouter()

router.include_router(tracking_router)
router.include_router(user_router)
router.include_router(permission_router)

# 后续API版本路由
router_v2 = APIRouter(prefix="/v2")
