from fastapi import Depends
from typing import Annotated
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base


db_url = "postgresql://postgres:admin@localhost:5432/full_stack_project_db"

engine = create_engine(db_url)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=True,
)

Base = declarative_base()


def of_get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(of_get_db)]
