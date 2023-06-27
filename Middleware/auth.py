#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    @File        :auth.py
    @Description :
    @DateTime    :2023/6/27 10:22 AM
    @Author      :Jay Zhang
"""

import time

from fastapi import FastAPI, Request
from starlette.responses import StreamingResponse, JSONResponse

app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    path = request.scope.get("path")
    print('path', path)
    token = request.headers.get("Authorization")
    print()
    # response: StreamingResponse = await call_next(request)
    # return response
    return JSONResponse(status_code=401, content={"message": "Unauthenticated"})
