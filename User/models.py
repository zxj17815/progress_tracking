#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    @File        :models.py
    @Description :
    @DateTime    :2023/6/27 9:08 AM
    @Author      :Jay Zhang
"""

from sqlalchemy import Column, Unicode, text, BigInteger
from sqlalchemy.dialects.mssql import TIMESTAMP
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
