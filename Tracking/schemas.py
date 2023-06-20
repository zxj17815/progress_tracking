#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    @File        :schemas.py
    @Description :
    @DateTime    :2023-06-16 15:43
    @Author      :Jay Zhang
"""
import datetime
from typing import Optional

from pydantic import BaseModel, Field


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
    remark_1: Optional[str] = Field(title="制一备注")
    start_time_2: Optional[int] = Field(title="开始时间制二,时间戳")
    end_time_2: Optional[int] = Field(title="结束时间制二,时间戳")
    remark_2: Optional[str] = Field(title="制二备注")
    start_time_3: Optional[int] = Field(title="开始时间制三,时间戳")
    end_time_3: Optional[int] = Field(title="结束时间制三,时间戳")
    remark_3: Optional[str] = Field(title="制三备注")
    start_time_4: Optional[int] = Field(title="开始时间制四,时间戳")
    end_time_4: Optional[int] = Field(title="结束时间制四,时间戳")
    remark_4: Optional[str] = Field(title="制四备注")
    work_time_type_id: Optional[str] = Field(title="工艺类型")

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
                "remark_1": "制一备注",
                "start_time_2": 1632892800,
                "end_time_2": 1632896400,
                "remark_2": "制二备注",
                "start_time_3": 1632892800,
                "end_time_3": 1632896400,
                "remark_3": "制三备注",
                "start_time_4": 1632892800,
                "end_time_4": 1632896400,
                "remark_4": "制四备注",
                "work_time_type_id": "LTV"
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


class TrackingR(BaseModel):
    order_id: Optional[str] = Field(default=..., title="销售单号")
    produce_id: Optional[str] = Field(default=..., title="生产订单号")
    cinv_code: Optional[str] = Field(default=..., title="存货编码")
    start_time_1: Optional[int] = Field(title="开始时间制一,时间戳")
    end_time_1: Optional[int] = Field(title="结束时间制一,时间戳")
    remark_1: Optional[str] = Field(title="制一备注")
    start_time_2: Optional[int] = Field(title="开始时间制二,时间戳")
    end_time_2: Optional[int] = Field(title="结束时间制二,时间戳")
    remark_2: Optional[str] = Field(title="制二备注")
    start_time_3: Optional[int] = Field(title="开始时间制三,时间戳")
    end_time_3: Optional[int] = Field(title="结束时间制三,时间戳")
    remark_3: Optional[str] = Field(title="制三备注")
    start_time_4: Optional[int] = Field(title="开始时间制四,时间戳")
    end_time_4: Optional[int] = Field(title="结束时间制四,时间戳")
    remark_4: Optional[str] = Field(title="制四备注")
    work_time_type_id: Optional[str] = Field(title="工艺类型")
    employee_id: Optional[str] = Field(title="员工id")
    employee_name: Optional[str] = Field(title="员工姓名")

    class Config:
        schema_extra = {
            "example": {
                "order_id": "SO2109290001",
                "produce_id": "MO2109290001",
                "cinv_code": "0101010001",
                "start_time_1": 1632892800,
                "end_time_1": 1632896400,
                "remark_1": "制一备注",
                "start_time_2": 1632892800,
                "end_time_2": 1632896400,
                "remark_2": "制二备注",
                "start_time_3": 1632892800,
                "end_time_3": 1632896400,
                "remark_3": "制三备注",
                "start_time_4": 1632892800,
                "end_time_4": 1632896400,
                "remark_4": "制四备注",
                "work_time_type_id": "LTV",
                "employee_id": "HX01234",
                "employee_name": "张三"
            }
        }


class CreateTracking(BaseModel):
    order_id: Optional[str] = Field(default=..., title="销售单号")
    produce_id: Optional[str] = Field(default=..., title="生产订单号")
    cinv_code: Optional[str] = Field(default=..., title="存货编码")
    start_time_1: Optional[int] = Field(title="开始时间制一,时间戳", le=9999999999)
    end_time_1: Optional[int] = Field(title="结束时间制一,时间戳", le=9999999999)
    remark_1: Optional[str] = Field(title="制一备注")
    start_time_2: Optional[int] = Field(title="开始时间制二,时间戳", le=9999999999)
    end_time_2: Optional[int] = Field(title="结束时间制二,时间戳", le=9999999999)
    remark_2: Optional[str] = Field(title="制二备注")
    start_time_3: Optional[int] = Field(title="开始时间制三,时间戳", le=9999999999)
    end_time_3: Optional[int] = Field(title="结束时间制三,时间戳", le=9999999999)
    remark_3: Optional[str] = Field(title="制三备注")
    start_time_4: Optional[int] = Field(title="开始时间制四,时间戳", le=9999999999)
    end_time_4: Optional[int] = Field(title="结束时间制四,时间戳", le=9999999999)
    remark_4: Optional[str] = Field(title="制四备注")
    work_time_type_id: Optional[str] = Field(title="工艺类型")
    employee_id: Optional[str] = Field(title="员工id")
    employee_name: Optional[str] = Field(title="员工姓名")

    class Config:
        schema_extra = {
            "example": {
                "order_id": "SO2109290001",
                "produce_id": "MO2109290001",
                "cinv_code": "0101010001",
                "start_time_1": 1632892800,
                "end_time_1": 1632896400,
                "remark_1": "制一备注",
                "start_time_2": 1632892800,
                "end_time_2": 1632896400,
                "remark_2": "制二备注",
                "start_time_3": 1632892800,
                "end_time_3": 1632896400,
                "remark_3": "制三备注",
                "start_time_4": 1632892800,
                "end_time_4": 1632896400,
                "remark_4": "制四备注",
                "work_time_type_id": "LTV",
                "employee_id": "HX01234",
                "employee_name": "张三"
            }
        }