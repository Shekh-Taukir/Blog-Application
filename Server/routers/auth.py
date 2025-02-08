from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from Server.db.db_init import db_dependency
from Server.db.models import User
from Server.db.schema import TokenModel
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from Server.routers.router_base import of_init_router

ls_api_prefix = "/auth"
lt_api_tags = ["Auth"]

SECRET_KEY = "e4f8b2d9c3a6e7f1b0d4c5a8f9e2t3c7d6a1e0f3c2b5d8a9e7f4b1c6d3a0e9f2"
ALGORITHM = "HS256"

auth_router = of_init_router(
    ls_api_prefix,
    lt_api_tags,
)

if auth_router is None:
    auth_router = APIRouter(
        prefix=ls_api_prefix,
        tags=[lt_api_tags[0]],
    )

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


def of_authenticate_user(as_user_id: str, as_pass: str, db):
    lb_flag = False
    db_user = db.query(User).filter(User.user_id == as_user_id).first()

    if db_user is None or not db_user:
        lb_flag = True
    else:
        if not bcrypt_context.verify(as_pass, db_user.password):
            lb_flag = True

    if lb_flag:
        return {"user_tran_id": -1, "user": None}

    return {"user_tran_id": db_user.tran_id, "user": db_user}


def of_create_access_token(user_tran_id: int, user_id: int, at_session_time):
    at_session_time = timedelta(at_session_time)

    encode = {"sub": user_id, "tran_id": user_tran_id}
    expires = datetime.utcnow() + at_session_time
    encode.update({"exp": expires})  # type:ignore

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def of_get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")  # type:ignore
        user_tran_id: int = payload.get("tran_id")  # type:ignore

        if user_id is None or user_tran_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate the user",
            )

        return {"user_id": user_id, "user_tran_id": user_tran_id}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate the user",
        )
    pass


@auth_router.post("/token", response_model=TokenModel)
async def of_login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency,
):
    li_result_data = of_authenticate_user(form_data.username, form_data.password, db)
    li_result = li_result_data.get("user_tran_id")

    if li_result < 0:  # type:ignore
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate the user",
        )
    user_data = li_result_data.get("user")

    token = of_create_access_token(
        user_tran_id=li_result,  # type:ignore
        user_id=user_data.user_id,  # type:ignore
        at_session_time=20,
    )

    return {"access_token": token, "token_type": "bearer"}
