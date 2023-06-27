#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    @File        :schemas.py
    @Description :
    @DateTime    :2023-06-16 15:01
    @Author      :Jay Zhang
"""
from typing import Optional

from pydantic import BaseModel, Field


class PermissionBase(BaseModel):
    id: Optional[int] = Field(description="权限ID")
    name: Optional[str] = Field(description="权限名称")

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "name": "tracking_p1_change"
            }
        }


class UserPermissionList(BaseModel):
    employee_id: str = Field(description="员工工号")
    permission: list[PermissionBase] = Field(description="权限列表")

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "employee_id": "HX05555",
                "permission": [
                    {
                        "id": 1,
                        "name": "tracking_p1_change"
                    }
                ]
            }
        }