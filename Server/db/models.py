from db.db_init import Base
from sqlalchemy import Integer, String, Column, ForeignKey, Date, DateTime, Text
from datetime import datetime, timezone


class User(Base):
    __tablename__ = "user_mst"

    tran_id = Column(Integer, primary_key=True)
    first_name = Column(String, index=True)
    last_name = Column(String)
    bdate = Column(Date)
    email = Column(String)
    user_id = Column(String, index=True)
    password = Column(String)

    def __str__(self):
        return "Object is " + self.first_name + ", " + self.last_name


class Blogs(Base):
    __tablename__ = "blog_mst"

    tran_id = Column(Integer, primary_key=True)
    blog_title = Column(String, index=True)
    blog_description = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    changed_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    created_by_user_id = Column(Integer, ForeignKey("user_mst.tran_id"))
