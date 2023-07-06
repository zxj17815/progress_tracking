#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    @File        :price.py
    @Description :
    @DateTime    :2023-01-12 16:15
    @Author      :Jay Zhang
"""
from tempfile import NamedTemporaryFile
from typing import List, Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from openpyxl import Workbook

from Db.database import ErpSessionLocal, SessionLocal
from Tracking.curd import get_mom, get_mom_detail, create_or_update_tracking, get_all_remark, create_remark, \
    update_remark_by_id, delete_remark
from Tracking.models import Tracking, TrackingLog, ReMark
from Tracking.schemas import ListMomOrderDetail, CreateTracking, ReMarkList, TrackingDetail, CreateReMark, ReMarkBase

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


@router.post("/order", response_model=TrackingDetail)
async def create_tracking(tracking: CreateTracking, erp_db: ErpSessionLocal = Depends(get_erp_db),
                          db: SessionLocal = Depends(get_db)):
    """
    新增进度数据
    :param erp_db:
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
    tracking_remark = tracking.pop('remark')
    tracking_obj = Tracking(**tracking)

    return create_or_update_tracking(db, tracking_obj, tracking_remark, tracking_log_obj)


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


@router.get("/remark", response_model=List[ReMarkList])
async def get_remark(db: SessionLocal = Depends(get_db),
                     remark_type: Annotated[str, Query(description="制造车间")] = None):
    """
    获取备注
    :param remark_type: 制造车间
    :param db:
    :return:
    """
    remark = get_all_remark(db, remark_type)
    return remark


@router.post("/remark", response_model=ReMarkBase)
async def add_remark(remark: CreateReMark, db: SessionLocal = Depends(get_db)):
    """
    新增备注
    :param remark:
    :param db:
    :return:
    """
    if remark.remark_type not in ["制一", "制二", "制三", "制四"]:
        raise HTTPException(status_code=400, detail=[
            {
                "loc": [
                    "body",
                    "remark_type"
                ],
                "msg": "remark_type is must in [制一, 制二, 制三, 制四]",
                "type": "value_error"
            }
        ])
    exist_obj = db.query(ReMark).filter(ReMark.delete_time == None,
                                        ReMark.remark_type == remark.remark_type,
                                        ReMark.description == remark.description).first()
    if exist_obj:
        raise HTTPException(status_code=400, detail=[
            {
                "loc": [
                    "body",
                    "description"
                ],
                "msg": "description is exist(id={0} key={1})".format(exist_obj.id, exist_obj.key),
                "type": "value_error"
            }
        ])
    remark_obj = ReMark(**remark.dict())
    return create_remark(db, remark_obj)


@router.put("/remark/{remark_id}", response_model=ReMarkBase)
async def update_remark(remark_id: int, remark: CreateReMark, db: SessionLocal = Depends(get_db)):
    """
    修改备注


    :param remark_id:
    :param remark:
    :param db:
    :return:
    """
    if remark.remark_type is not None and remark.remark_type not in ["制一", "制二", "制三", "制四"]:
        raise HTTPException(status_code=400, detail=[
            {
                "loc": [
                    "body",
                    "remark_type"
                ],
                "msg": "remark_type is must in [制一, 制二, 制三, 制四]",
                "type": "value_error"
            }
        ])
    exist_obj = db.query(ReMark).filter(ReMark.id == remark_id).first()
    if not exist_obj:
        raise HTTPException(status_code=400, detail=[
            {
                "loc": [
                    "body",
                    "remark_id"
                ],
                "msg": "remark_id is not exist",
                "type": "value_error"
            }
        ])

    return update_remark_by_id(db, remark_id, ReMark(**remark.dict()))


@router.delete("/remark/{remark_id}", response_model=ReMarkBase)
async def delete_remark_by_id(remark_id: int, db: SessionLocal = Depends(get_db)):
    """
    删除备注
    :param remark_id:
    :param db:
    :return:
    """
    exist_obj = db.query(ReMark).filter(ReMark.id == remark_id).first()
    if not exist_obj:
        raise HTTPException(status_code=400, detail=[
            {
                "loc": [
                    "body",
                    "remark_id"
                ],
                "msg": "remark is not exist",
                "type": "value_error"
            }
        ])
    try:
        return delete_remark(db, exist_obj)
    except Exception as e:
        raise HTTPException(status_code=400, detail=[
            {
                "loc": [
                    "body",
                    "remark_id"
                ],
                "msg": str(e),
                "type": "value_error"
            }
        ])
