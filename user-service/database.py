from beanie import init_beanie
import motor.motor_asyncio
from config import get_settings

from core.models import User

settings = get_settings()
client = motor.motor_asyncio.AsyncIOMotorClient(
    f"{settings.mongo_host}:{settings.mongo_port}"
)


async def init_db():
    await init_beanie(database=client.main_db, document_models=[User])
