#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    @File        :config.py
    @Description :
    @DateTime    :2023/6/20 1:57 PM
    @Author      :Jay Zhang
"""
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    redis_url: str
    sqlalchemy_database_url: str
    erp_sqlalchemy_database_url: str
    dd_sqlalchemy_database_url: str
    dd_url: str
    dd_app_key: str
    dd_app_secret: str

    class Config:
        env_file = ".env", ".env.dev", ".env.prod"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
