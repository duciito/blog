import asyncio
from contextlib import asynccontextmanager

from core.routes import router as CoreRouter
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from notifications.tasks import consume_like_events
from services.database import init_db
from services.redis import get_redis_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    # Start independent consumers in the background
    loop = asyncio.get_event_loop()
    loop.create_task(consume_like_events(redis=get_redis_client()))
    yield


app = FastAPI(title="User service", lifespan=lifespan)
app.include_router(CoreRouter, prefix="/api")
app.mount("/static", StaticFiles(directory="src/static"), name="static")
