from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers.user_router import user_router

from .routers.blog_router import blog_router
from .db.db_init import Base, engine
from .routers.auth import auth_router

app = FastAPI()

app.include_router(user_router)
app.include_router(blog_router)
app.include_router(auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
