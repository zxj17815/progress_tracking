#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    @File        :start.py
    @Description :
    @DateTime    :2022-12-05 11:08
    @Author      :Jay Zhang
"""

from fastapi import APIRouter

router = APIRouter(prefix="/User", tags=["dingding"])
router.include_router(user_info_router)
router.include_router(call_back_router)
router.include_router(base_router)
router.include_router(employee_router)
router.include_router(department_router)
