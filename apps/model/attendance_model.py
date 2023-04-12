from apps.config.db import Base
from sqlalchemy import Column,Integer,Boolean,DateTime,String
from sqlalchemy.schema import ForeignKey

from datetime import datetime


class Attendace(Base):
    __tablename__='attendace'
    id =  Column(Integer,primary_key=True,autoincrement=True)
    attendace_date=Column(DateTime)
    notebook=Column(Boolean,default=False)
    bible=Column(Boolean,default=False)
    uniform=Column(Boolean,default=False)
    offering=Column(Boolean,default=False)
    initial_letter = Column(String)
    user_id=Column(Integer,ForeignKey("user.id",ondelete="CASCADE"))
    is_active = Column(Boolean,default=True)
    created_at=Column(DateTime,default=datetime.now,onupdate=datetime.now)