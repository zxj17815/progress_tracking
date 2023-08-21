#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    @File        :database.py
    @Description :
    @DateTime    :2022-11-26 13:27
    @Author      :Jay Zhang
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from redis import StrictRedis, ConnectionPool
import config

CONFIG = config.get_settings()

REDIS_URL = CONFIG.redis_url

ERP_SQLALCHEMY_DATABASE_URL = CONFIG.erp_sqlalchemy_database_url

erp_engine = create_engine(ERP_SQLALCHEMY_DATABASE_URL)

ErpSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=erp_engine)

DD_SQLALCHEMY_DATABASE_URL = CONFIG.dd_sqlalchemy_database_url

dd_engine = create_engine(DD_SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, pool_recycle=3600)

DdSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=dd_engine)

SQLALCHEMY_DATABASE_URL = CONFIG.sqlalchemy_database_url

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# redis 连接
pool = ConnectionPool.from_url(REDIS_URL, decode_responses=True)
redis = StrictRedis(connection_pool=pool)
