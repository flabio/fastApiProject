from apps.config.db import Base
from sqlalchemy import Column,Integer,String,Text,Boolean,DateTime
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


class MinisterialAcademyUser(Base):
    __tablename__='ministerial_academy_user'
    id = Column(Integer,primary_key=True,autoincrement=True,nullable=True)
    date_academy=Column(DateTime)
    place=Column(Text)
    user_id=Column(Integer,ForeignKey("user.id",ondelete="CASCADE"))
    #user = relationship("User",back_populates="ministerialacademyuser")
    ministerial_academy_id=Column(Integer,ForeignKey("ministerial_academy.id",ondelete="CASCADE"))
    #ministerial_academy = relationship("ministerialacademy",back_populates="ministerial_academy_user")
    is_active = Column(Boolean,default=True)
    created_at=Column(DateTime,default=datetime.now,onupdate=datetime.now)