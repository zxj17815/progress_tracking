from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from Middleware.auth import add_process_time_header
from Tracking.controllers import router as tracking_router
from User.controllers import router as user_router

app = FastAPI()

app.include_router(tracking_router)
app.include_router(user_router)

# CORS 跨域共享
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.add_middleware(
#     BaseHTTPMiddleware,
#     dispatch=add_process_time_header,
# )

#
# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request, exc):
#     err_str = ""
#     for err in exc.errors():
#         print(err["loc"][1])
#         err_str += f"{err['loc'][1]}:{err['msg']};"
#     return PlainTextResponse(err_str, status_code=400)
# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
