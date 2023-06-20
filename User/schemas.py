#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    @File        :user_info_schema.py
    @Description :
    @DateTime    :2023-06-16 15:01
    @Author      :Jay Zhang
"""
from typing import Optional

from pydantic import BaseModel, Field


class UserInfo(BaseModel):
    user_id: Optional[str] = Field(title="钉钉UUID")
    employee_name: Optional[str] = Field(title="员工姓名")
    employee_id: Optional[str] = Field(title="员工ID")
    dept: Optional[str] = Field(title="部门")

    class Config:
        schema_extra = {
            "example": {
                "user_id": "876asd87as78d68a7s6d",
                "employee_name": "张三",
                "employee_id": "HX01234",
                "dept": "技术部"
            }
        }
