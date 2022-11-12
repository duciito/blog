from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from core.auth import jwt_required_async

from core.routes import router as CoreRouter
from database import init_db

app = FastAPI(title="User service")


@app.on_event("startup")
async def start_db():
    # Make jwt_required async so we can check token validity in Redis.
    AuthJWT.jwt_required_async = jwt_required_async
    await init_db()


@app.exception_handler(AuthJWTException)
def auth_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={'detail': exc.message}
    )


app.include_router(CoreRouter, prefix='/api')
