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
from Tracking.models import MomOrder, MomOrderDetail, Inventory, Tracking, TrackingLog, ReMark, TrackingReMark


def get_mom(db: Session, order_id: str = None, produce_id: str = None,
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
        SELECT count(t1.status) as count
    '''

    sql = '''
        SELECT
            t6.id as tracking_id,
            t6.order_id,
            t6.start_time_1,
            t6.end_time_1,
            t7.work_time_1 as plan_time_1,
            (end_time_1-start_time_1)/86400+1 as actual_time_1,
            t6.start_time_2,
            t6.end_time_2,
            t7.work_time_2 as plan_time_2,
            (end_time_2-start_time_2)/86400+1 as actual_time_2,
            t6.start_time_3,
            t6.end_time_3,
            t7.work_time_3 as plan_time_3,
            (end_time_3-start_time_3)/86400+1 as actual_time_3,
            t6.start_time_4,
            t6.end_time_4,
            t7.work_time_4 as plan_time_4,
            (end_time_4-start_time_4)/86400+1 as actual_time_4,
            t6.work_time_type_id,
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
            LEFT JOIN work_time t7 ON t6.work_time_type_id= t7.name
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
    data = [dict(i) for i in data]
    for item in data:
        if item["tracking_id"] is not None:
            remarks = db.query(TrackingReMark).filter(TrackingReMark.tracking_id == item["tracking_id"]).all()
            item["remark"] = [
                {"remark_type": i.remark.remark_type, "key": i.remark.key, "remark_id": i.remark_id,
                 "parent_id": i.remark.parent_id, "description": i.remark.description,
                 "customer_remark": i.customer_remark if i.remark.allow_edit else None} for i in remarks]
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


def create_or_update_tracking(db: Session, tracking: Tracking, tracking_remark: list[TrackingReMark],
                              tracking_log: TrackingLog):
    """
    添加活更新工单追溯条
    """
    remarks = []
    if tracking_remark is not None:
        for item in tracking_remark:
            print(item)
            remark = db.query(ReMark).filter(ReMark.id == item["remark_id"]).first()
            if remark:
                temp_obj = TrackingReMark(remark_id=remark.id, create_time=int(time.time()))
                if remark.allow_edit:
                    temp_obj.customer_remark = item["customer_remark"]
                remarks.append(temp_obj)

    tracking_data = db.query(Tracking).filter(Tracking.order_id == tracking.order_id,
                                              Tracking.produce_id == tracking.produce_id,
                                              Tracking.cinv_code == tracking.cinv_code).first()
    if tracking_data:
        if tracking.start_time_1:
            tracking_data.start_time_1 = tracking.start_time_1
        if tracking.end_time_1:
            tracking_data.end_time_1 = tracking.end_time_1
        if tracking.start_time_2:
            tracking_data.start_time_2 = tracking.start_time_2
        if tracking.end_time_2:
            tracking_data.end_time_2 = tracking.end_time_2
        if tracking.start_time_3:
            tracking_data.start_time_3 = tracking.start_time_3
        if tracking.end_time_3:
            tracking_data.end_time_3 = tracking.end_time_3
        if tracking.start_time_4:
            tracking_data.start_time_4 = tracking.start_time_4
        if tracking.end_time_4:
            tracking_data.end_time_4 = tracking.end_time_4
        if tracking.work_time_type_id:
            tracking_data.work_time_type_id = tracking.work_time_type_id
        tracking = tracking_data
        tracking.remark = remarks
        tracking_log.timestamp = time.time()
        tracking_log.action_type = "change"
        tracking_dict = copy.deepcopy(tracking.__dict__)
        tracking_dict.pop("_sa_instance_state")
        tracking_dict["remark"] = [i.remark_id for i in tracking.remark]
        tracking_log.source_data = json.dumps(tracking_dict)
        tracking.tracking_logs.append(tracking_log)
    else:
        tracking.remark = remarks
        tracking_log.timestamp = time.time()
        tracking_log.action_type = "add"
        tracking_dict = copy.deepcopy(tracking.__dict__)
        tracking_dict.pop("_sa_instance_state")
        tracking_dict["remark"] = [i.remark_id for i in tracking.remark]
        tracking_log.source_data = json.dumps(tracking_dict)
        tracking.tracking_logs.append(tracking_log)
        db.add(tracking)
    db.commit()
    db.refresh(tracking)
    print(tracking.remark)
    return tracking


def get_all_remark(db: Session, remark_type: str = None, is_parent: bool = True):
    """
    获取所有备注
    """
    query = db.query(ReMark).filter(ReMark.delete_time.is_(None))
    if remark_type:
        query = query.filter(ReMark.remark_type == remark_type)
    if is_parent:
        query = query.filter(ReMark.parent_id == 0)
    data = query.all()
    return data


def create_remark(db: Session, remark: ReMark):
    """
    创建备注
    """
    remark.create_time = int(time.time())
    remark.update_time = int(time.time())
    db.add(remark)
    db.flush()
    remark.key = "{0}-{1}".format(remark.parent_id, remark.id)
    db.commit()
    db.refresh(remark)
    return remark


def update_remark_by_id(db: Session, remark_id: int, remark: ReMark):
    """
    更新备注
    """
    obj: ReMark = db.query(ReMark).get(remark_id)
    if remark.remark_type:
        obj.remark_type = remark.remark_type
    if remark.description:
        obj.description = remark.description
    if remark.parent_id:
        obj.parent_id = remark.parent_id
        obj.key = "{0}-{1}".format(obj.parent_id, obj.id)
    if remark.allow_edit is not None:
        obj.allow_edit = remark.allow_edit
    obj.update_time = int(time.time())
    db.commit()
    db.refresh(obj)
    return obj


def delete_remark(db: Session, remark: ReMark):
    """
    删除备注
    """
    remark.delete_time = int(time.time())
    db.commit()
    return remark
