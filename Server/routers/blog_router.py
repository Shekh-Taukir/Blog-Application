from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from starlette import status

from Server.db.models import Blogs
from Server.db.db_init import db_dependency
from Server.db.schema import BlogsModel

from .router_base import of_result_message, of_init_router


ls_api_prefix = "/blogs"
lt_api_tags = ["Blog"]

blog_router = of_init_router(
    ls_api_prefix,
    lt_api_tags,
)

if blog_router is None:
    blog_router = APIRouter(
        prefix=ls_api_prefix,
        tags=[lt_api_tags[0]],
    )


@blog_router.get("/All Blogs")
async def of_get_all_blogs(db: db_dependency):
    # old logic to retrieve the list of blogs

    # lu_blogs = db.query(Blogs).order_by(Blogs.tran_id.desc()).all()
    lu_blogs = db.execute(text("select * from of_get_blogs()")).mappings().all()

    if len(lu_blogs) == 0:
        return HTTPException(
            status_code=status.HTTP_204_NO_CONTENT, detail="No blog data found"
        )

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

    return of_result_message(True, None, new_blog, True)


@blog_router.get("/Get Blog")
async def of_get_blog(blog_id: int, db: db_dependency):
    if blog_id <= 0:
        return of_result_message(False, "blog_id is not valid.")

    result = (
        db.execute(text("select * from of_get_blogs(:blog_id)"), {"blog_id": blog_id})
        .mappings()
        .fetchone()
    )

    if result is None:
        return of_result_message(False, "Data as per blog_id not found")

    return of_result_message(True, None, result)


@blog_router.post("/Update Blog")
async def of_update_blog(blog_id: int, blog_data: BlogsModel, db: db_dependency):
    if blog_id <= 0:
        return of_result_message(False, "blog_id is not valid")

    if blog_data is None:
        return of_result_message(False, "blog inputted data is not valid")

    blog = db.query(Blogs).filter(Blogs.tran_id == blog_id).first()

    if blog is None or not blog:
        return of_result_message(False, "blog data as per blog_id is not valid")

    blog.blog_title = blog_data.blogs_title  # type:ignore
    blog.blog_description = blog_data.blogs_description  # type:ignore

    db.commit()
    db.refresh(blog)

    return of_result_message(True, "", blog)


@blog_router.delete("/Delete Blog")
async def of_delete_blog(blog_id: int, db: db_dependency):
    if blog_id <= 0:
        return of_result_message(False, "blog_id is not valid")

    blog = db.query(Blogs).filter(Blogs.tran_id == blog_id).first()

    if blog is None or not blog:
        return of_result_message(False, "blog data as per blog_id is not valid")

    db.delete(blog)
    db.commit()

    return of_result_message(True, "Blog deleted as blog_id")
