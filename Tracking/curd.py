#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    @File        :price.py
    @Description :价格表查询
    @DateTime    :2023-01-12 14:07
    @Author      :Jay Zhang
"""
import copy
import json
import time

from sqlalchemy import text
from sqlalchemy.orm import Session
from Tracking.models import MomOrder, MomOrderDetail, Inventory, Tracking, TrackingLog


def get_mom(erp_db: Session, db: Session, order_id: str = None, produce_id: str = None,
            cinv_code: str = None, status: [int] = None,
            begin_date: str = None, end_date: str = None,
            skip: int = 0, limit: int = 20):
    """
    获取工单
    """
    if order_id:
        order_id = "%" + order_id + "%"
    else:
        order_id = "%%"

    if produce_id:
        produce_id = "%" + produce_id + "%"
    else:
        produce_id = "%%"

    if cinv_code:
        cinv_code = "%" + cinv_code + "%"
    else:
        cinv_code = "%%"

    count_sql = '''
        SELECT count(*) as count
    '''

    sql = '''
        SELECT
            t6.*,
            t6.id as tracking_id,
            t3.mocode as produce_id,
            t5.cSOCode as order_id,
            t1.qty as qty,
            t1.status as status,
            t3.createtime as create_time,
            t2.cinvcode as cinv_code,
            t2.cinvname as cinv_name,
            t1.define32 as spec
        '''

    sql_from = '''
        FROM
            ufdata_001_2018..mom_orderdetail t1
            LEFT JOIN ufdata_001_2018..Inventory t2 ON t1.invcode= t2.cinvcode
            LEFT JOIN ufdata_001_2018..mom_order t3 ON t1.moid= t3.moid
            LEFT JOIN ufdata_001_2018..SO_SODetails t4 ON t1.OrderDid= t4.iSOsID
            LEFT JOIN ufdata_001_2018..SO_SOMain t5 on t4.id=t5.id
            LEFT JOIN tracking t6 ON t1.invcode= t6.inv_code AND t3.mocode= t6.produce_id AND t5.cSOCode= t6.order_id
        WHERE t5.cSOCode like :order_id
        AND t3.mocode like :produce_id
        AND t2.cinvcode like :cinv_code'''

    sql = sql + sql_from

    count_sql = count_sql + sql_from

    params = {"order_id": order_id, "produce_id": produce_id, "cinv_code": cinv_code}

    if begin_date is not None and end_date is not None:
        sql = sql + '''
        AND t3.createtime >= :begin_date
        AND t3.createtime <= :end_date
        '''
        count_sql = count_sql + '''
        AND t3.createtime >= :begin_date
        AND t3.createtime <= :end_date
        '''
        params["begin_date"] = begin_date
        params["end_date"] = end_date

    if status is not None:
        sql = sql + '''
        AND t1.status in :status
        '''
        count_sql = count_sql + '''
        AND t1.status in :status
        '''
        params["status"] = status

    if skip < 0:
        sql = sql + '''
        ORDER BY
            t3.createtime desc
        '''
    else:
        sql = sql + '''
            ORDER BY
                t3.createtime desc
            offset :offset rows fetch next :next rows only
            '''
        params["offset"] = skip
        params["next"] = limit

    data = db.execute(
        text(sql), params=params).all()
    count = db.execute(
        text(count_sql), params=params).first()["count"]

    return count, data


def get_mom_detail(erp_db: Session, order_id: str = None, produce_id: str = None, cinv_code: str = None):
    """
    获取工单明细
    """

    data = erp_db.query(MomOrderDetail).filter(MomOrder.MoCode == produce_id,
                                               MomOrderDetail.OrderCode == order_id,
                                               MomOrderDetail.InvCode == cinv_code).first()
    return data


def get_tracking(db: Session, skip: int = 0, limit: int = 20):
    """
    获取工单追溯条
    """
    count = db.query(Tracking).count()
    data = db.query(Tracking).order_by(Tracking.id).offset(skip).limit(limit).all()
    return count, data


def create_or_update_tracking(db: Session, tracking: Tracking, tracking_log: TrackingLog):
    """
    添加活更新工单追溯条
    """
    tracking_data = db.query(Tracking).filter(Tracking.order_id == tracking.order_id,
                                              Tracking.produce_id == tracking.produce_id,
                                              Tracking.cinv_code == tracking.cinv_code).first()
    print(tracking.start_time_1)
    if tracking_data:
        if tracking.start_time_1:
            tracking_data.start_time_1 = tracking.start_time_1
        if tracking.end_time_1:
            tracking_data.end_time_1 = tracking.end_time_1
        if tracking.remark_1 is not None:
            tracking_data.remark_1 = tracking.remark_1
        if tracking.start_time_2:
            tracking_data.start_time_2 = tracking.start_time_2
        if tracking.end_time_2:
            tracking_data.end_time_2 = tracking.end_time_2
        if tracking.remark_2 is not None:
            tracking_data.remark_2 = tracking.remark_2
        if tracking.start_time_3:
            tracking_data.start_time_3 = tracking.start_time_3
        if tracking.end_time_3:
            tracking_data.end_time_3 = tracking.end_time_3
        if tracking.remark_3 is not None:
            tracking_data.remark_3 = tracking.remark_3
        if tracking.start_time_4:
            tracking_data.start_time_4 = tracking.start_time_4
        if tracking.end_time_4:
            tracking_data.end_time_4 = tracking.end_time_4
        if tracking.remark_4 is not None:
            tracking_data.remark_4 = tracking.remark_4
        if tracking.work_time_type_id:
            tracking_data.work_time_type_id = tracking.work_time_type_id
        tracking = tracking_data
        tracking_log.timestamp = time.time()
        tracking_log.action_type = "change"
        tracking_dict = copy.deepcopy(tracking.__dict__)
        tracking_dict.pop("_sa_instance_state")
        tracking_log.source_data = json.dumps(tracking_dict)
        tracking.tracking_logs.append(tracking_log)
    else:
        tracking_log.timestamp = time.time()
        tracking_log.action_type = "add"
        tracking_dict = copy.deepcopy(tracking.__dict__)
        tracking_dict.pop("_sa_instance_state")
        tracking_log.source_data = json.dumps(tracking_dict)
        tracking.tracking_logs.append(tracking_log)
        db.add(tracking)
    db.commit()
    db.refresh(tracking)
    return tracking
