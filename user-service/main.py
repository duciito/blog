from fastapi import FastAPI, APIRouter

from database import init_db

app = FastAPI(title="User service")


@app.on_event("startup")
async def start_db():
    await init_db()
