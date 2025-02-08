from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated
from starlette import status

from Server.db.schema import UserModel, LoginModel
from Server.db.models import User
from Server.db.db_init import db_dependency

from .router_base import of_result_message, of_init_router
from .auth import bcrypt_context, auth_router, of_authenticate_user, of_get_current_user

ls_api_prefix = "/user"
lt_api_tags = ["User"]

user_router = of_init_router(
    ls_api_prefix,
    lt_api_tags,
)

if user_router is None:
    user_router = APIRouter(
        prefix=ls_api_prefix,
        tags=[lt_api_tags[0]],
    )


user_dependency = Annotated[dict, Depends(of_get_current_user)]


# @user_router.post("/add_user")
@auth_router.post("/add_user", status_code=status.HTTP_201_CREATED)
async def of_add_user(user: UserModel, db: db_dependency):
    if not user:
        return of_result_message(False, "Not valid input user data")

    db_user_id = db.query(User).filter(User.user_id == user.user_id).first()

    if db_user_id:
        return of_result_message(False, "Entered user_id already exists")

    db_user_email = db.query(User).filter(User.email == user.email).first()

    if db_user_email:
        return of_result_message(False, "Entered email already exists")

    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        bdate=user.bdate,
        email=user.email,
        user_id=user.user_id,
        password=bcrypt_context.hash(user.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return of_result_message(True, None, new_user, True)


@user_router.post("/login_user")
async def of_login_user(login_user: LoginModel, db: db_dependency):

    as_user_id = login_user.user_id.strip()
    as_pass = login_user.password.strip()

    if len(as_user_id) == 0 or len(as_pass) == 0:
        return of_result_message(False, "User_id or Password is not valid.")

    li_result = of_authenticate_user(as_user_id, as_pass, db).get("user_tran_id")

    if li_result < 0:  # type:ignore
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user.",
        )

    return of_result_message(True, None, {"login_user": li_result})


@user_router.get("/get_user")
async def of_get_user(user_tran_id: int, db: db_dependency):
    if user_tran_id <= 0:
        return of_result_message(False, "user_tran_id is invalid.")

    db_user = db.query(User).filter(User.tran_id == user_tran_id).first()

    print(db_user)
    if db_user is None or not db_user:
        return of_result_message(False, "user not found as per id.")

    return of_result_message(True, None, db_user)


@user_router.post("/update_user")
async def of_update_user(user_tran_id: int, update_user: UserModel, db: db_dependency):
    if user_tran_id <= 0:
        return of_result_message(False, "user_tran_id is not valid")

    if update_user is None:
        return of_result_message(False, "user_data is not valid.")

    db_user = db.query(User).filter(User.tran_id == user_tran_id).first()

    if db_user is None:
        return of_result_message(False, "User data is not valid as per user_tran_id.")

    db_user.first_name = update_user.first_name  # type: ignore
    db_user.last_name = update_user.last_name  # type: ignore
    db_user.email = update_user.email  # type: ignore
    db_user.bdate = update_user.bdate  # type: ignore

    db.commit()
    db.refresh(db_user)

    return of_result_message(True, "User data updated")


@user_router.delete("/Delete User")
async def of_delete_user(user_tran_id: int, db: db_dependency):
    if user_tran_id <= 0:
        return of_result_message(False, "User_tran_id is not valid.")

    db_user = db.query(User).filter(User.tran_id == user_tran_id).first()

    if db_user is None:
        return of_result_message(False, "User data from user_id is not proper")

    db.delete(db_user)
    db.commit()

    return of_result_message(True, "User is deleted of provided user_id")


@user_router.get("/get_user1")
async def of_get_user_auth(user: user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return of_result_message(True, "", {"user": user})
