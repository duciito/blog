from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi_jwt_auth import AuthJWT
from fastapi_mail import FastMail, MessageSchema, MessageType
from pydantic import EmailStr
from config import get_email_config
from core.auth import create_access_token, create_tokens

from core.models import User
from core.schemas import LoginSchema, PasswordChangeSchema, TokensSchema
from core.utils import ses_verify_email_address

router = APIRouter(prefix='/auth', tags=["Auth"])


@router.post("/signup", response_model=TokensSchema, status_code=201)
async def signup(user: User, auth: AuthJWT = Depends()):
    # Check for email availability
    existing_user = await User.find_one({'email': user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail='Email already taken.')
    created_user = await user.create()

    # Verify user's email.
    await ses_verify_email_address(created_user.email)
    return create_tokens(created_user, auth)


@router.post("/login", response_model=TokensSchema)
async def login(login: LoginSchema, auth: AuthJWT = Depends()):
    user = await User.find_one({'email': login.email})
    if not user:
        raise HTTPException(status_code=400, detail='No user exists with that email.')
    if not user.check_password(login.password):
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

# TODO: token invocation (sign out) with Redis denylist.


@router.post("/password_change", status_code=204)
async def password_change(data: PasswordChangeSchema, auth: AuthJWT = Depends()):
    auth.jwt_required()
    user = await User.get(auth.get_jwt_subject())

    if not user:
        raise HTTPException(status_code=401, detail='No user associated with this token was found.')
    if not user.check_password(data.current_password):
        raise HTTPException(status_code=400, detail='Current password does not match.')

    await user.set_password(data.new_password, save=True)


@router.post("/password_reset", status_code=204)
async def password_reset(email: EmailStr, redirect_url: str, req: Request):
    user = User.find_one({'email': email})

    if not user:
        raise HTTPException(status_code=400, detail='No user exists with that email.')
    # Unique token associated with this reset attempt.
    # We store this associated with the user id for 24h.
    token = uuid4().hex
    verify_url = req.url_for('password_reset_verify')
    # Construct verify route url to redirect the user back to the API
    # for link validity check.
    absolute_url = f'{verify_url}?token={token}&redirect_url={redirect_url}'
    # Send email to the user
    message = MessageSchema(
        subject='Reset your password',
        recipients=[email],
        body=f'Click the link below to reset password.\n{absolute_url}',
        subtype=MessageType.plain
    )
    fm = FastMail(get_email_config())
    try:
        await fm.send_message(message)
    except:
        raise HTTPException(status_code=400, detail="Couldn't send email. Check that it is verified.")


@router.get("/password_reset_verify")
async def password_reset_verify():
    pass
