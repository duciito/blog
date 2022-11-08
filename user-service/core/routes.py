from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from core.auth import create_tokens

from core.models import User
from core.schemas import TokensSchema
from core.utils import hash_password

router = APIRouter(prefix='/auth', tags=["Auth"])


@router.post("/signup", response_model=TokensSchema, status_code=201)
async def signup(user: User):
    # Check for email availability
    existing_user = await User.find_one({'email': user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail='Email already taken.')
    created_user = await user.create()
    # TODO: ses email verify logic

    tokens = create_tokens(created_user)
    return tokens
