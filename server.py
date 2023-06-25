#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    @File        :server.py
    @Description :启动服务
    @DateTime    :2023-06-18 15:25
    @Author      :Jay Zhang
"""
from multiprocessing import cpu_count

import uvicorn


def start_server(host="127.0.0.1",
                 port=5055,
                 num_workers=4,
                 loop="asyncio",
                 reload=False):
    uvicorn.run("main:app",
                host=host,
                port=port,
                workers=num_workers,
                loop=loop,
                log_config="uvicorn_config.json",
                reload=reload)


if __name__ == "__main__":
    num_workers = int(cpu_count() * 0.75)
    start_server(num_workers=num_workers)
