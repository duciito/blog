import logging
from typing import Annotated
from uuid import uuid4

from config import get_email_config
from core.auth import DENYLIST_PREFIX, AuthDep, create_access_token, create_tokens
from core.models import User
from core.schemas import (
    AuthToken,
    LoginSchema,
    PasswordChangeSchema,
    PasswordResetSchema,
    TokensSchema,
)
from core.tasks import add_user_to_stream
from core.utils import get_user_from_reset_token, ses_verify_email_address
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi_mail import FastMail, MessageSchema, MessageType
from pydantic import EmailStr
from redis import RedisError
from redis import asyncio as aioredis
from redis_conf import get_redis_client

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup", response_model=TokensSchema, status_code=201)
async def signup(
    user: User,
    bg: BackgroundTasks,
    redis: aioredis.Redis = Depends(get_redis_client),
):
    # Check for email availability
    existing_user = await User.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already taken.")
    created_user = await user.create()

    # Send verification email in the background
    # and notify other services of new user creation.
    bg.add_task(ses_verify_email_address, created_user.email)
    bg.add_task(add_user_to_stream, created_user, redis)
    return create_tokens(created_user)


@router.post("/login", response_model=TokensSchema)
async def login(login: LoginSchema):
    user = await User.find_one({"email": login.email})
    if not user:
        raise HTTPException(status_code=400, detail="No user exists with that email.")
    if not user.check_password(login.password):
        raise HTTPException(status_code=400, detail="Invalid password.")

    return create_tokens(user)


@router.post("/refresh", response_model=TokensSchema)
async def refresh(
    auth_token: Annotated[AuthToken, Depends(AuthDep(token_type="refresh"))],
):
    user = await User.get(auth_token.user_id)

    if not user:
        raise HTTPException(
            status_code=401, detail="No user associated with this token was found."
        )

    return TokensSchema(
        access_token=create_access_token(user), refresh_token=auth_token.encoded
    )


@router.post("/logout", status_code=204)
async def logout(
    auth_token: Annotated[AuthToken, Depends(AuthDep())],
    redis: aioredis.Redis = Depends(get_redis_client),
):
    token_id, expires_at = auth_token.payload["jti"], auth_token.payload["exp"]
    await redis.set(f"{DENYLIST_PREFIX}:{token_id}", 1, exat=expires_at)


@router.post("/password_change", status_code=204)
async def password_change(
    data: PasswordChangeSchema, auth_token: Annotated[AuthToken, Depends(AuthDep())]
):
    user = await User.get(auth_token.user_id)

    if not user:
        raise HTTPException(
            status_code=401, detail="No user associated with this token was found."
        )
    if not user.check_password(data.current_password):
        raise HTTPException(status_code=400, detail="Current password does not match.")

    await user.set_password(data.new_password, save=True)


@router.post("/password_reset", status_code=204)
async def password_reset(
    email: EmailStr,
    redirect_url: str,
    req: Request,
    redis: aioredis.Redis = Depends(get_redis_client),
):
    user = await User.find_one({"email": email})

    if not user:
        raise HTTPException(status_code=400, detail="No user exists with that email.")
    # Unique token associated with this reset attempt.
    # We store this associated with the user id for 24h.
    token = uuid4().hex
    verify_url = req.url_for("password_reset_verify")
    # Construct verify route url to redirect the user back to the API
    # for link validity check.
    if not redirect_url.startswith("http://"):
        redirect_url = f"http://{redirect_url}"
    absolute_url = f"{verify_url}?token={token}&redirect_url={redirect_url}"
    # Send email to the user
    message = MessageSchema(
        subject="Reset your password",
        recipients=[email],
        body=f"Click the link below to reset password.\n{absolute_url}",
        subtype=MessageType.plain,
    )
    fm = FastMail(get_email_config())
    try:
        # Keep token associated with the user for 24h.
        await redis.set(f"pw-reset:{token}", str(user.id), ex=86400)
        await fm.send_message(message)
    except RedisError as e:
        logger.error(f"Couldn't save reset token to Redis: {e}")
        raise HTTPException(
            status_code=502, detail="Couldn't process request. Please try again."
        ) from e
    except:  # noqa
        raise HTTPException(
            status_code=400, detail="Couldn't send email. Check that it is verified."
        ) from None


@router.get("/password_reset_verify")
async def password_reset_verify(
    token: str, redirect_url: str, redis: aioredis.Redis = Depends(get_redis_client)
):
    user, reason = await get_user_from_reset_token(token, redis)
    get_params = {"token_valid": bool(user), "token": token}
    if reason:
        get_params["reason"] = reason

    redirect_url += "?"
    for param, value in get_params.items():
        redirect_url += f"{param}={value}&"

    return RedirectResponse(redirect_url, status_code=303)


@router.post("/password_reset_data", status_code=204)
async def password_reset_data(
    data: PasswordResetSchema, redis: aioredis.Redis = Depends(get_redis_client)
):
    user, reason = await get_user_from_reset_token(data.token, redis)
    if not user:
        raise HTTPException(status_code=400, detail=reason)

    await user.set_password(data.password, save=True)
