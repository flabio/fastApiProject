from apps.config.db import Base
from sqlalchemy import Column,Boolean,Integer,Text,String,DateTime
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class SubDetachment(Base):
    __tablename__ = 'subdetachment'
    id = Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String)
    image = Column(Text)
    is_active=Column(Boolean,default=True)
    created_at=Column(DateTime,default=datetime.now,onupdate=datetime.now)
