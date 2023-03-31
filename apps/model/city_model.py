from apps.config.db import Base
from sqlalchemy import Column,Integer,String,Text,Boolean,DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


class City(Base):
    __tablename__='city'
    id = Column(Integer,primary_key=True,autoincrement=True)
    name=Column(Text)
    postal_code=Column(String(20))
    is_active = Column(Boolean,default=True)
    created_at=Column(DateTime,default=datetime.now,onupdate=datetime.now)
    user = relationship("User", back_populates="city")