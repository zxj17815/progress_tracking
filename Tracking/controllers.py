#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    @File        :price.py
    @Description :
    @DateTime    :2023-01-12 16:15
    @Author      :Jay Zhang
"""
from typing import List, Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from openpyxl.styles import Alignment

from Db.database import ErpSessionLocal, SessionLocal
from Tracking.curd import get_mom, get_mom_detail, create_or_update_tracking
from Tracking.models import Tracking, TrackingLog, ReMarkType
from Tracking.schemas import ListMomOrderDetail, CreateTracking, ReMarkTypeBase
from openpyxl import Workbook
from tempfile import NamedTemporaryFile

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
async def get_tracking(db: SessionLocal = Depends(get_db),
                       order_id: Annotated[str, Query(description="销售订单号")] = None,
                       produce_id: Annotated[str, Query(description="生产单号")] = None,
                       cinv_code: Annotated[str, Query(description="物料编码")] = None,
                       status: Annotated[List[int], Query(description="状态")] = None,
                       begin_date: Annotated[str, Query(description="开始日期")] = None,
                       end_date: Annotated[str, Query(description="结束日期")] = None,
                       page: Annotated[int, Query(description="页码")] = 1,
                       page_size: Annotated[int, Query(description="每页数量")] = 20):
    count, data = get_mom(db, order_id, produce_id, cinv_code, status,
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


@router.get("/order/file")
async def get_tracking_file(db: SessionLocal = Depends(get_db),
                            order_id: Annotated[str, Query(description="销售订单号")] = None,
                            produce_id: Annotated[str, Query(description="生产单号")] = None,
                            cinv_code: Annotated[str, Query(description="物料编码")] = None,
                            status: Annotated[List[int], Query(description="状态")] = None,
                            begin_date: Annotated[str, Query(description="开始日期")] = None,
                            end_date: Annotated[str, Query(description="结束日期")] = None):
    """
    获取进度文件
    :param db:
    :param order_id:
    :param produce_id:
    :param cinv_code:
    :param status:
    :param begin_date:
    :param end_date:
    :return:
    """
    count, data = get_mom(db, order_id, produce_id, cinv_code, status,
                          begin_date, end_date, 0, 1000000)
    wb = Workbook()
    ws = wb.active
    ws.append(
        ['销售订单号', '生产单号', '物料编码', '物料名称', '规格型号', '生产数量', '创建日期', '状态',
         '工艺路线', '制一', '制二', '制三', '制四', '求和'])

    for item in data:
        temp1 = """耗时: {0}天\n标准耗时：{1}\n开工：{2}\n完工：{3}""".format(item.actual_time_1, item.plan_time_1,
                                                                           item.start_time_1, item.end_time_1)
        temp2 = """耗时: {0}天\n标准耗时：{1}\n开工：{2}\n完工：{3}""".format(item.actual_time_2, item.plan_time_2,
                                                                           item.start_time_2, item.end_time_2)
        temp3 = """耗时: {0}天\n标准耗时：{1}\n开工：{2}\n完工：{3}""".format(item.actual_time_3, item.plan_time_3,
                                                                           item.start_time_3, item.end_time_3)
        temp4 = """耗时: {0}天\n标准耗时：{1}\n开工：{2}\n完工：{3}""".format(item.actual_time_4, item.plan_time_4,
                                                                           item.start_time_4, item.end_time_4)

        ws.append(
            [item.order_id, item.produce_id, item.cinv_code, item.cinv_name, item.spec, item.qty, item.create_time,
             item.status, item.work_time_type_id, temp1, temp2, temp3, temp4])

    def stream_file():
        with NamedTemporaryFile() as tmp:
            wb.save(tmp.name)
            tmp.seek(0)
            stream = tmp.read()
        yield stream

    return StreamingResponse(stream_file(),
                             media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                             headers={'Content-Disposition': 'attachment; filename=tracking.xlsx'})


@router.get("/remark", response_model=List[ReMarkTypeBase])
async def get_tracking_file(db: SessionLocal = Depends(get_db)):
    """
    获取备注
    :param db:
    :return:
    """
    remark = db.query(ReMarkType).all()
    return remark
