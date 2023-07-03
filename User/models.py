#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    @File        :models.py
    @Description :
    @DateTime    :2023/6/27 9:08 AM
    @Author      :Jay Zhang
"""

from sqlalchemy import Column, Unicode, text, BigInteger, Integer, String, DateTime
from sqlalchemy.dialects.mssql import TIMESTAMP
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship

from Db.database import Base
from Permission.models import Permission

metadata = Base.metadata


class User(Base):
    __tablename__ = 'user'
    id = Column(BigInteger, primary_key=True)
    dd_id = Column(Unicode(150), nullable=True, unique=True)
    employee_id = Column(Unicode(150), nullable=True, unique=True)
    # status = Column(TINYINT, nullable=False)
    create_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    update_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'))
    permission = relationship(Permission, secondary="user_permission", backref="user")


class Department(Base):
    __tablename__ = 'dd_departments'

    dept_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50, 'utf8mb4_general_ci'), nullable=False)
    description = Column(String(255, 'utf8mb4_general_ci'))
    created_at = Column(DateTime, index=True)
    updated_at = Column(DateTime, index=True)
    parent_id = Column(Integer, index=True)


class Employee(Base):
    __tablename__ = 'dd_employees'

    user_id = Column(String(50, 'utf8mb4_general_ci'), primary_key=True, index=True)
    employee_id = Column('job_number', String(50, 'utf8mb4_general_ci'), unique=True)
    name = Column(String(50, 'utf8mb4_general_ci'), nullable=False)
    avatar = Column(String(255, 'utf8mb4_general_ci'))
    active = Column(TINYINT)
