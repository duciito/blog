from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from core.auth import create_access_token, create_tokens

from core.models import User
from core.schemas import LoginSchema, TokensSchema
from core.utils import hash_password

router = APIRouter(prefix='/auth', tags=["Auth"])


@router.post("/signup", response_model=TokensSchema, status_code=201)
async def signup(user: User, auth: AuthJWT = Depends()):
    # Check for email availability
    existing_user = await User.find_one({'email': user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail='Email already taken.')
    created_user = await user.create()
    # TODO: ses email verify logic

    return create_tokens(created_user, auth)


@router.post("/login", response_model=TokensSchema)
async def login(login: LoginSchema, auth: AuthJWT = Depends()):
    user = await User.find_one({'email': login.email})
    if not user:
        raise HTTPException(status_code=400, detail='No user exists with that email.')
    if hash_password(login.password) != user.password:
        raise HTTPException(status_code=400, detail='Invalid password.')

    return create_tokens(user, auth)


@router.post("/refresh", response_model=TokensSchema)
async def refresh(auth: AuthJWT = Depends()):
    auth.jwt_refresh_token_required()
    user = await User.get(auth.get_jwt_subject())

    if not user:
        raise HTTPException(status_code=401, detail='No user associated with this token was found.')

    return TokensSchema(
        access_token=create_access_token(user, auth),
        refresh_token=auth._token
    )
