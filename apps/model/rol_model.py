from apps.config.db import Base
from sqlalchemy import Column,Integer,String,Boolean,DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


class Rol(Base):
    __tablename__='rol'
    id = Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String)
    is_active = Column(Boolean,default=True)
    created_at=Column(DateTime,default=datetime.now,onupdate=datetime.now)
    user = relationship("User", back_populates="rol")