#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    @File        :schemas.py
    @Description :
    @DateTime    :2023-06-16 15:43
    @Author      :Jay Zhang
"""
import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ReMarkBase(BaseModel):
    id: Optional[int] = Field(title="id")
    key: Optional[str] = Field(title="备注编码")
    parent_id: Optional[int] = Field(title="父级id")
    description: Optional[str] = Field(title="备注内容")
    allow_edit: Optional[bool] = Field(title="是否允许自定义编辑")

    class Config:
        orm_mode = True


class ReMarkList(BaseModel):
    id: Optional[int] = Field(title="id")
    key: Optional[str] = Field(title="备注编码")
    parent_id: Optional[int] = Field(title="父级id")
    remark_type: Optional[str] = Field(title="车间")
    description: Optional[str] = Field(title="备注内容")
    children: Optional[list[ReMarkBase]] = Field(title="备注内容")
    allow_edit: Optional[bool] = Field(title="是否允许自定义编辑")

    class Config:
        orm_mode = True


class TrackingReMarkCreate(BaseModel):
    remark_id: Optional[int] = Field(title="id")
    customer_remark: Optional[str] = Field(title="自定义备注")

    class Config:
        orm_mode = True


class TrackingReMark(TrackingReMarkCreate):
    key: Optional[str] = Field(title="备注编码")
    parent_id: Optional[int] = Field(title="父级id")
    remark_type: Optional[str] = Field(title="车间")
    description: Optional[str] = Field(title="备注内容")


class Inventory(BaseModel):
    InvCode: str = None
    InvName: str = None

    class Config:
        orm_mode = True


class MomOrder(BaseModel):
    MoDId: str = None

    class Config:
        orm_mode = True


class MomOrderDetail(BaseModel):
    order_id: int = None
    # MoId: Optional[int] = Field(alias='moId')
    qty: float = None
    status: int = None
    cinv_code: str = None
    cinv_name: str = None

    class Config:
        orm_mode = True


class MomTracking(BaseModel):
    order_id: Optional[str] = Field(title="销售单号")
    produce_id: Optional[str] = Field(title="生产订单号")
    spec: Optional[str] = Field(title="规格型号")
    qty: Optional[float] = Field(title="订单数量")
    status: Optional[int] = Field(title="订单状态")
    create_time: Optional[datetime.date] = Field(title="创建时间")
    cinv_code: Optional[str] = Field(title="存货编码")
    cinv_name: Optional[str] = Field(title="存货名称")
    tracking_id: Optional[int] = Field(title="跟踪数据id")
    start_time_1: Optional[int] = Field(title="开始时间制一,时间戳")
    end_time_1: Optional[int] = Field(title="结束时间制一,时间戳")
    plan_time_1: Optional[int] = Field(title="计划时间制一,天")
    actual_time_1: Optional[int] = Field(title="实际时间制一,天")
    start_time_2: Optional[int] = Field(title="开始时间制二,时间戳")
    end_time_2: Optional[int] = Field(title="结束时间制二,时间戳")
    plan_time_2: Optional[int] = Field(title="计划时间制二,天")
    actual_time_2: Optional[int] = Field(title="实际时间制二,天")
    start_time_3: Optional[int] = Field(title="开始时间制三,时间戳")
    end_time_3: Optional[int] = Field(title="结束时间制三,时间戳")
    plan_time_3: Optional[int] = Field(title="计划时间制三,天")
    actual_time_3: Optional[int] = Field(title="实际时间制三,天")
    start_time_4: Optional[int] = Field(title="开始时间制四,时间戳")
    end_time_4: Optional[int] = Field(title="结束时间制四,时间戳")
    plan_time_4: Optional[int] = Field(title="计划时间制四,天")
    actual_time_4: Optional[int] = Field(title="实际时间制四,天")
    work_time_type_id: Optional[str] = Field(title="工艺类型")
    remark: Optional[list[TrackingReMark]] = Field(title="备注")

    class Config:
        schema_extra = {
            "example": {
                "order_id": "SO2109290001",
                "produce_id": "MO2109290001",
                "spec": "规格-型号",
                "qty": 100,
                "status": 1,
                "create_time": "2022-10-10",
                "cinv_code": "0101010001",
                "cinv_name": "存货名称",
                "tracking_id": 1,
                "start_time_1": 1632892800,
                "end_time_1": 1632896400,
                "plan_time_1": 3,
                "actual_time_1": 1,
                "start_time_2": 1632892800,
                "end_time_2": 1632896400,
                "plan_time_2": 3,
                "actual_time_2": 2,
                "start_time_3": 1632892800,
                "end_time_3": 1632896400,
                "plan_time_3": 3,
                "actual_time_3": 5,
                "start_time_4": 1632892800,
                "end_time_4": 1632896400,
                "plan_time_4": 3,
                "actual_time_4": 2,
                "work_time_type_id": "LTV",
                "remark": [
                    {
                        "remark_type": "制一",
                        "remark_id": 1,
                        "description": "质量问题",
                        "customer_remark": "null"
                    },
                    {
                        "remark_type": "制二",
                        "remark_id": 68,
                        "description": "其他",
                        "customer_remark": "其他的自定义备注"
                    }
                ]
            }
        }


class ListMomOrderDetail(BaseModel):
    total: Optional[int] = Field(title="总数")
    result: list[MomTracking] = None
    page: Optional[int] = Field(title="页码")


class CreateTrackingLog(BaseModel):
    employee_id: Optional[int] = Field(title="员工id")
    employee_name: Optional[str] = Field(title="员工姓名")

    class Config:
        orm_mode = True


class TrackingDetail(BaseModel):
    order_id: Optional[str] = Field(title="销售单号")
    produce_id: Optional[str] = Field(title="生产订单号")
    cinv_code: Optional[str] = Field(title="存货编码")
    start_time_1: Optional[int] = Field(title="开始时间制一,时间戳", le=9999999999)
    end_time_1: Optional[int] = Field(title="结束时间制一,时间戳", le=9999999999)
    start_time_2: Optional[int] = Field(title="开始时间制二,时间戳", le=9999999999)
    end_time_2: Optional[int] = Field(title="结束时间制二,时间戳", le=9999999999)
    start_time_3: Optional[int] = Field(title="开始时间制三,时间戳", le=9999999999)
    end_time_3: Optional[int] = Field(title="结束时间制三,时间戳", le=9999999999)
    start_time_4: Optional[int] = Field(title="开始时间制四,时间戳", le=9999999999)
    end_time_4: Optional[int] = Field(title="结束时间制四,时间戳", le=9999999999)
    work_time_type_id: Optional[str] = Field(title="工艺类型")
    remark: Optional[list[TrackingReMarkCreate]] = Field(title="备注")

    class Config:
        orm_mode = True


class CreateTracking(BaseModel):
    order_id: Optional[str] = Field(default=..., title="销售单号")
    produce_id: Optional[str] = Field(default=..., title="生产订单号")
    cinv_code: Optional[str] = Field(default=..., title="存货编码")
    start_time_1: Optional[int] = Field(title="开始时间制一,时间戳", le=9999999999)
    end_time_1: Optional[int] = Field(title="结束时间制一,时间戳", le=9999999999)
    start_time_2: Optional[int] = Field(title="开始时间制二,时间戳", le=9999999999)
    end_time_2: Optional[int] = Field(title="结束时间制二,时间戳", le=9999999999)
    start_time_3: Optional[int] = Field(title="开始时间制三,时间戳", le=9999999999)
    end_time_3: Optional[int] = Field(title="结束时间制三,时间戳", le=9999999999)
    start_time_4: Optional[int] = Field(title="开始时间制四,时间戳", le=9999999999)
    end_time_4: Optional[int] = Field(title="结束时间制四,时间戳", le=9999999999)
    work_time_type_id: Optional[str] = Field(title="工艺类型")
    remark: Optional[list[TrackingReMarkCreate]] = Field(title="备注")
    employee_id: Optional[str] = Field(title="员工id")
    employee_name: Optional[str] = Field(title="员工姓名")

    class Config:
        schema_extra = {
            "example": {
                "order_id": "23JMJ0006-1-YB",
                "produce_id": "0000149047",
                "cinv_code": "0304034033",
                "start_time_1": 1632892800,
                "end_time_1": 1632896400,
                "start_time_2": 1632892800,
                "end_time_2": 1632896400,
                "start_time_3": 1632892800,
                "end_time_3": 1632896400,
                "start_time_4": 1632892800,
                "end_time_4": 1632896400,
                "work_time_type_id": "LTV",
                "remark": [
                    {
                        "remark_id": 1,
                        "customer_remark": "null",
                    },
                    {
                        "remark_id": 68,
                        "customer_remark": "akjsdhuiawhd",
                    }
                ],
                "employee_id": "HX01234",
                "employee_name": "张三"
            }
        }


class CreateReMark(BaseModel):
    parent_id: Optional[int] = Field(title="父级id")
    remark_type: Optional[str] = Field(title="车间,(制一、制二、制三、制四)")
    description: Optional[str] = Field(title="备注描述")
    allow_edit: Optional[bool] = Field(False, title="是否允许编辑")

    class Config:
        orm_mode = True
