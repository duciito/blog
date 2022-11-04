from fastapi import APIRouter

from core.models import User
from core.utils import hash_password

router = APIRouter(prefix='/auth', tags=["Auth"])


@router.post("/signup")
async def signup(user: User):
    user.password = hash_password(user.password)
    created_user = await user.create()
    return created_user
