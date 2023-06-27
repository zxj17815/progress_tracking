#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    @File        :models.py
    @Description :
    @DateTime    :2023/6/27 10:13 AM
    @Author      :Jay Zhang
"""

from sqlalchemy import Boolean, Column, DECIMAL, DateTime, Float, ForeignKey, Index, Integer, Unicode, text, BigInteger, \
    func, Table
from sqlalchemy.dialects.mssql import TIMESTAMP, TINYINT
from sqlalchemy.orm import relationship
from Db.database import Base

metadata = Base.metadata


class Permission(Base):
    __tablename__ = 'permission'
    id = Column(BigInteger, primary_key=True)
    name = Column(Unicode(150), nullable=False, unique=True)
    # path = Column(Unicode(150), nullable=True)
    # status = Column(TINYINT, nullable=False)
    description = Column(Unicode(255), nullable=True)
    create_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    update_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'))


user_permission = Table(
    'user_permission', metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permission.id'), primary_key=True)
)
