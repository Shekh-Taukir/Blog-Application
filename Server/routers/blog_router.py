from fastapi import APIRouter
from db.models import Blogs
from db.db_init import db_dependency
from typing import Optional
from db.schema import BlogsModel


blog_router = APIRouter(
    prefix="/blogs",
    tags=["Blog"],
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


@blog_router.get("/All Blogs")
async def of_get_all_blogs(db: db_dependency):
    lu_blogs = db.query(Blogs).order_by(Blogs.tran_id.desc()).all()

    return of_result_message(True, None, lu_blogs)


@blog_router.post("/Create Blog")
async def of_create_blog(user_id: int, blog: BlogsModel, db: db_dependency):
    if user_id <= 0:
        return of_result_message(False, "user_id is not valid")

    if blog is None:
        return of_result_message(False, "Blog inputted data is not valid.")

    new_blog = Blogs(
        blog_title=blog.blogs_title,
        blog_description=blog.blogs_description,
        created_by_user_id=user_id,
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return of_result_message(True, None, new_blog)
