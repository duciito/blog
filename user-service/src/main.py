import asyncio
from contextlib import asynccontextmanager

from core.auth import jwt_required_async
from core.routes import router as CoreRouter
from database import init_db
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from notifications.tasks import consume_like_events
from redis_conf import get_redis_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Make jwt_required async so we can check token validity in Redis.
    AuthJWT.jwt_required_async = jwt_required_async
    await init_db()
    # Start independent consumers in the background
    loop = asyncio.get_event_loop()
    loop.create_task(consume_like_events(redis=get_redis_client()))
    yield


app = FastAPI(title="User service", lifespan=lifespan)


@app.exception_handler(AuthJWTException)
def auth_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


app.include_router(CoreRouter, prefix="/api")
app.mount("/static", StaticFiles(directory="src/static"), name="static")
