from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api_version_router import router, router_v2

app = FastAPI()

# 路由导入
app.include_router(router)
app.include_router(router_v2)

# CORS 跨域共享
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 鉴权中间件
# app.add_middleware(
#     BaseHTTPMiddleware,
#     dispatch=add_process_time_header,
# )
