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
from User.models import User, Employee


def get_permission(db: Session, user: User):
    return User


def get_all_employee_permission(db: Session, dd_db: Session):
    data = []
    employees = dd_db.query(Employee).filter(Employee.employee_id != "").all()
    for employee in employees:
        user = db.query(User).filter(User.employee_id == employee.employee_id).first()
        if user:
            data.append({
                "employee_name": employee.name,
                "employee_id": employee.employee_id,
                "permission": user.permission
            })
        else:
            data.append({
                "employee_name": employee.name,
                "employee_id": employee.employee_id,
                "permission": []
            })
    return data
