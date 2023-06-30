#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    @File        :models.py
    @Description :
    @DateTime    :2023/6/14 1:24 PM
    @Author      :Jay Zhang
"""

# sqlacodegen mssql+pymssql://sa:jxbs-1934@192.168.1.92/ufdata_001_2018 > test_model.py --tables mom_order

from sqlalchemy import Boolean, Column, DECIMAL, DateTime, Float, ForeignKey, Index, Integer, Unicode, text, BigInteger
from sqlalchemy.dialects.mssql import TIMESTAMP, TINYINT
from sqlalchemy.orm import relationship, backref
from Db.database import Base

metadata = Base.metadata


class MomOrder(Base):
    __tablename__ = 'mom_order'
    __table_args__ = (
        Index('idx_mom_order_1', 'MoCode', 'MoId'),
    )

    MoId = Column(Integer, primary_key=True)
    MoCode = Column(Unicode(30), nullable=False, unique=True)
    CreateDate = Column(DateTime)
    CreateUser = Column(Unicode(20))
    ModifyDate = Column(DateTime)
    ModifyUser = Column(Unicode(20))
    UpdCount = Column(Integer, server_default=text("(0)"))
    Ufts = Column(TIMESTAMP)
    Define1 = Column(Unicode(20))
    Define2 = Column(Unicode(20))
    Define3 = Column(Unicode(20))
    Define4 = Column(DateTime)
    Define5 = Column(Integer)
    Define6 = Column(DateTime)
    Define7 = Column(Float(53))
    Define8 = Column(Unicode(4))
    Define9 = Column(Unicode(8))
    Define10 = Column(Unicode(60))
    Define11 = Column(Unicode(120))
    Define12 = Column(Unicode(120))
    Define13 = Column(Unicode(120))
    Define14 = Column(Unicode(120))
    Define15 = Column(Integer)
    Define16 = Column(Float(53))
    VTid = Column(Integer)
    CreateTime = Column(DateTime)
    ModifyTime = Column(DateTime)
    iPrintCount = Column(Integer, server_default=text("(0)"))
    RelsVTid = Column(Integer)
    cSysBarCode = Column(Unicode(60))


class MomOrderDetail(Base):
    __tablename__ = 'mom_orderdetail'
    __table_args__ = (
        Index('i_mom_orderdetail_1', 'OrderDId', 'OrderType'),
        Index('idx_mom_orderdetail_1', 'PartId', 'RoutingId'),
        Index('i_mom_orderdetail_2', 'MoId', 'MoDId'),
        Index('i_mom_orderdetail', 'MoId', 'Status')
    )

    MoDId = Column('MoDId', Integer, primary_key=True)
    mo_id = Column('MoId', ForeignKey('mom_order.MoId'), nullable=False)
    SortSeq = Column(Integer, nullable=False, server_default=text("(0)"))
    MoClass = Column(TINYINT, server_default=text("(1)"))
    MoTypeId = Column(Integer)
    qty = Column('Qty', DECIMAL(28, 6), server_default=text("""create default D_Udt_QTY as 0"""))
    MrpQty = Column(DECIMAL(28, 6), server_default=text("""create default D_Udt_QTY as 0"""))
    AuxUnitCode = Column(Unicode(35))
    AuxQty = Column(DECIMAL(28, 6), server_default=text("""create default D_Udt_QTY as 0"""))
    ChangeRate = Column(DECIMAL(22, 6), server_default=text("""create default D_Udt_ChangeRate as 0"""))
    MoLotCode = Column(Unicode(60))
    WhCode = Column(Unicode(10))
    MDeptCode = Column(Unicode(12))
    SoType = Column(TINYINT, server_default=text("(0)"))
    SoDId = Column(Unicode(30))
    SoCode = Column(Unicode(30))
    SoSeq = Column(Integer, server_default=text("(0)"))
    DeclaredQty = Column(DECIMAL(28, 6), server_default=text("""create default D_Udt_QTY as 0"""))
    QualifiedInQty = Column(DECIMAL(28, 6), server_default=text("""create default D_Udt_QTY as 0"""))
    status = Column('Status', TINYINT, server_default=text("(1)"))
    OrgStatus = Column(TINYINT, server_default=text("(1)"))
    BomId = Column(Integer)
    RoutingId = Column(Integer)  # 工艺路线类型
    CustBomId = Column(Integer)
    DemandId = Column(Integer, index=True)
    PlanCode = Column(Unicode(20))
    PartId = Column(Integer, index=True)
    InvCode = Column(Unicode(60), index=True)
    Free1 = Column(Unicode(20))
    Free2 = Column(Unicode(20))
    Free3 = Column(Unicode(20))
    Free4 = Column(Unicode(20))
    Free5 = Column(Unicode(20))
    Free6 = Column(Unicode(20))
    Free7 = Column(Unicode(20))
    Free8 = Column(Unicode(20))
    Free9 = Column(Unicode(20))
    Free10 = Column(Unicode(20))
    SfcFlag = Column(Boolean, server_default=text("(0)"))
    CrpFlag = Column(Boolean, server_default=text("(0)"))
    QcFlag = Column(Boolean, server_default=text("(0)"))
    RelsDate = Column(DateTime)
    RelsUser = Column(Unicode(20))
    CloseDate = Column(DateTime)
    OrgClsDate = Column(DateTime)
    Ufts = Column(TIMESTAMP, index=True)
    Define22 = Column(Unicode(60))
    Define23 = Column(Unicode(60))
    Define24 = Column(Unicode(60))
    Define25 = Column(Unicode(60))
    Define26 = Column(Float(53))
    Define27 = Column(Float(53))
    Define28 = Column(Unicode(120))
    Define29 = Column(Unicode(120))
    Define30 = Column(Unicode(120))
    Define31 = Column(Unicode(120))
    Define32 = Column(Unicode(120))
    Define33 = Column(Unicode(120))
    Define34 = Column(Integer)
    Define35 = Column(Integer)
    Define36 = Column(DateTime)
    Define37 = Column(DateTime)
    LeadTime = Column(Integer, server_default=text("(0)"))
    OpScheduleType = Column(TINYINT, server_default=text("(1)"))
    OrdFlag = Column(Boolean, server_default=text("(0)"))
    WIPType = Column(TINYINT, server_default=text("(5)"))
    SupplyWhCode = Column(Unicode(10))
    ReasonCode = Column(Unicode(10))
    IsWFControlled = Column(TINYINT, server_default=text("(0)"))
    iVerifyState = Column(Integer, server_default=text("(0)"))
    iReturnCount = Column(Integer, server_default=text("(0)"))
    Remark = Column(Unicode(255))
    SourceMoCode = Column(Unicode(30))
    SourceMoSeq = Column(Integer)
    SourceMoId = Column(Integer, server_default=text("(0)"))
    SourceMoDId = Column(Integer, server_default=text("(0)"))
    SourceQCCode = Column(Unicode(30))
    SourceQCId = Column(Integer, server_default=text("(0)"))
    SourceQCDId = Column(Integer, server_default=text("(0)"))
    CostItemCode = Column(Unicode(60))
    CostItemName = Column(Unicode(255))
    RelsTime = Column(DateTime)
    CloseUser = Column(Unicode(20))
    CloseTime = Column(DateTime)
    OrgClsTime = Column(DateTime)
    AuditStatus = Column(TINYINT, server_default=text("(1)"))
    PAllocateId = Column(Integer, server_default=text("(0)"))
    DemandCode = Column(Unicode(30))
    CollectiveFlag = Column(TINYINT, server_default=text("(0)"))
    OrderType = Column(TINYINT, index=True, server_default=text("(0)"))
    OrderDId = Column(Integer, server_default=text("(0)"))
    OrderCode = Column(Unicode(30))
    OrderSeq = Column(Integer, server_default=text("(0)"))
    ManualCode = Column(Unicode(30))
    ReformFlag = Column(Boolean, server_default=text("(0)"))
    SourceQCVouchType = Column(TINYINT, server_default=text("(0)"))
    OrgQty = Column(DECIMAL(28, 6), server_default=text("""create default D_Udt_QTY as 0"""))
    FmFlag = Column(Boolean, server_default=text("(0)"))
    MinSN = Column(Unicode(200))
    MaxSN = Column(Unicode(200))
    SourceSvcCode = Column(Unicode(30))
    SourceSvcId = Column(Unicode(80))
    SourceSvcDId = Column(Unicode(80))
    BomType = Column(TINYINT, server_default=text("(0)"))
    RoutingType = Column(TINYINT, server_default=text("(0)"))
    BusFlowId = Column(Integer)
    RunCardFlag = Column(Boolean, server_default=text("(0)"))
    RequisitionFlag = Column(Boolean, server_default=text("(0)"))
    AlloVTid = Column(Integer)
    RelsAlloVTid = Column(Integer)
    iPrintCount = Column(Integer, server_default=text("(0)"))
    cbSysBarCode = Column(Unicode(80))
    cCurrentAuditor = Column(Unicode(200))
    CustCode = Column(Unicode(20))
    LPlanCode = Column(Unicode(40))
    SourceSvcVouchType = Column(TINYINT, server_default=text("(0)"))
    FactoryCode = Column(Unicode(50))
    PlanCodeBatUpdData = Column(Unicode(4000))

    mom_order = relationship('MomOrder')
    # inventory = relationship('Inventory')


class Inventory(Base):
    __tablename__ = 'Inventory'

    cinv_code = Column('cinvCode', Unicode(60), primary_key=True)
    cinv_name = Column('cinvName', Unicode(120))


class Tracking(Base):
    __tablename__ = 'tracking'

    id = Column(BigInteger, primary_key=True)
    order_id = Column(Unicode(150))
    produce_id = Column(Unicode(150))
    cinv_code = Column('inv_code', Unicode(150))
    start_time_1 = Column(Integer)
    end_time_1 = Column(Integer)
    start_time_2 = Column(Integer)
    end_time_2 = Column(Integer)
    start_time_3 = Column(Integer)
    end_time_3 = Column(Integer)
    start_time_4 = Column(Integer)
    end_time_4 = Column(Integer)
    work_time_type_id = Column(Unicode(200))
    remark = relationship('TrackingReMark')
    tracking_logs = relationship('TrackingLog')


class TrackingLog(Base):
    __tablename__ = 'tracking_log'

    id = Column(BigInteger, primary_key=True)
    tracking_id = Column(BigInteger, ForeignKey('tracking.id'))
    employee_id = Column(Unicode(20))
    employee_name = Column(Unicode(20))
    source_data = Column(Unicode(2000))
    action_type = Column(Unicode(20))
    timestamp = Column(Integer)


class ReMark(Base):
    __tablename__ = 'remark'

    id = Column(BigInteger, primary_key=True)
    parent_id = Column(BigInteger, ForeignKey('remark.id'))
    remark_type = Column(Unicode(150))
    description = Column(Unicode(500))
    allow_edit = Column(Boolean, server_default=text("(0)"))
    key = Column(Unicode(250))
    create_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    update_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'))
    children = relationship('ReMark', backref=backref('parent', remote_side=[id]))


class TrackingReMark(Base):
    __tablename__ = 'tracking_remark'

    id = Column(BigInteger, primary_key=True)
    tracking_id = Column(BigInteger, ForeignKey('tracking.id'))
    remark_id = Column(BigInteger, ForeignKey('remark.id'))
    customer_remark = Column(Unicode(500))
    create_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    remark = relationship('ReMark')
