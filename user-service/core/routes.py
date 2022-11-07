from fastapi import APIRouter, HTTPException
from pydantic import ValidationError

from core.models import User
from core.utils import hash_password

router = APIRouter(prefix='/auth', tags=["Auth"])


@router.post("/signup")
async def signup(user: User):
    # Check for email availability
    existing_user = User.find_one(User.email == user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail='Email already taken.')
    created_user = await user.create()

    # TODO: ses email verify logic
    return created_user
