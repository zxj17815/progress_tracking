#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    @File        :price.py
    @Description :价格表查询
    @DateTime    :2023-01-12 14:07
    @Author      :Jay Zhang
"""

from sqlalchemy.orm import Session

from Permission.models import Permission
from Tracking.models import Tracking
from User.models import User


def get_permission(db: Session, user: User):
    return User
