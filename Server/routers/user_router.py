from fastapi import APIRouter
from db.schema import UserModel, LoginModel
from db.models import User
from db.db_init import db_dependency
from sqlalchemy import and_
from typing import Optional

user_router = APIRouter(
    prefix="/user",
    tags=["User"],
)


def of_result_message(
    ab_success: bool,
    as_message: Optional[str] = None,
    alt_result=None,
):
    ld_return = {}

    ld_return["Success"] = ab_success

    if as_message:
        ld_return["Message"] = as_message

    if alt_result:
        ld_return["result"] = alt_result
        ld_return["no_of_entries"] = len(alt_result)

    return ld_return


@user_router.post("/add_user")
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
        password=user.password,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return of_result_message(True, None, new_user)


@user_router.post("/login_user")
async def of_login_user(login_user: LoginModel, db: db_dependency):

    as_user_id = login_user.user_id.strip()
    as_pass = login_user.password.strip()

    if len(as_user_id) == 0 or len(as_pass) == 0:
        return of_result_message(False, "User_id or Password is not valid.")

    db_user = (
        db.query(User)
        .filter(and_(User.user_id == as_user_id, User.password == as_pass))
        .first()
    )

    if db_user is None:
        return of_result_message(False)

    if db_user:
        return of_result_message(True, None, {"login_user": db_user.tran_id})
    else:
        return of_result_message(False)


@user_router.get("/get_user")
async def of_get_user(user_tran_id: int, db: db_dependency):
    if user_tran_id <= 0:
        return of_result_message(False, "user_tran_id is invalid.")

    db_user = db.query(User).filter(User.tran_id == user_tran_id).first()

    if db_user is None:
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
