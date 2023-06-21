#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    @File        :price.py
    @Description :
    @DateTime    :2023-01-12 16:15
    @Author      :Jay Zhang
"""
from typing import Union, List, Annotated

from fastapi import APIRouter, Depends, HTTPException, Header, Query
from pydantic import ValidationError

from Tracking.models import Tracking, TrackingLog
from Db.database import ErpSessionLocal, SessionLocal
from Tracking.curd import get_mom, get_mom_detail, create_or_update_tracking
from Tracking.schemas import ListMomOrderDetail, CreateTracking

router = APIRouter(prefix="/tracking")


# Dependency
def get_erp_db():
    db = ErpSessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/order", response_model=ListMomOrderDetail)
async def get_tracking(erp_db: ErpSessionLocal = Depends(get_erp_db),
                       db: SessionLocal = Depends(get_db),
                       order_id: Annotated[str, Query(description="销售订单号")] = None,
                       produce_id: Annotated[str, Query(description="生产单号")] = None,
                       cinv_code: Annotated[str, Query(description="物料编码")] = None,
                       status: Annotated[List[int], Query(description="状态")] = None,
                       begin_date: Annotated[str, Query(description="开始日期")] = None,
                       end_date: Annotated[str, Query(description="结束日期")] = None,
                       page: Annotated[int, Query(description="页码")] = 1,
                       page_size: Annotated[int, Query(description="每页数量")] = 20):
    count, data = get_mom(erp_db, db, order_id, produce_id, cinv_code, status,
                          begin_date, end_date,
                          (page - 1) * page_size, page_size)

    return {"result": data, "total": count, "page": page}


@router.post("/order")
async def create_tracking(tracking: CreateTracking, erp_db: ErpSessionLocal = Depends(get_erp_db),
                          db: SessionLocal = Depends(get_db)):
    """
    新增进度数据
    :param tracking:
    :param db:
    :return:
    """
    mom_obj = get_mom_detail(erp_db, tracking.order_id, tracking.produce_id, tracking.cinv_code)
    if not mom_obj:
        raise HTTPException(status_code=400, detail=[
            {
                "loc": [
                    "body",
                    "order_id"
                ],
                "msg": "order is not exist",
                "type": "value_error.missing"
            }
        ])

    tracking_log_obj = TrackingLog(employee_id=tracking.employee_id, employee_name=tracking.employee_name)
    tracking = tracking.dict()
    tracking.pop('employee_id')
    tracking.pop('employee_name')
    tracking_obj = Tracking(**tracking)

    return create_or_update_tracking(db, tracking_obj, tracking_log_obj)
