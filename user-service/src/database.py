import motor.motor_asyncio
from beanie import init_beanie
from config import get_settings
from core.models import User


async def init_db():
    settings = get_settings()
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo_url)
    await init_beanie(database=client.main_db, document_models=[User])
