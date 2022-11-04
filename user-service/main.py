from fastapi import FastAPI

from core.routes import router as CoreRouter
from database import init_db

app = FastAPI(title="User service")


@app.on_event("startup")
async def start_db():
    await init_db()


app.include_router(CoreRouter, prefix='/api')
