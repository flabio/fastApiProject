from apps.config.db import Base
from sqlalchemy import Column,Boolean,Integer,String,DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


class Church(Base):
    __tablename__ = 'church'
    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String)
    email=Column(String)
    address=Column(String)
    telephone=Column(String)
    user=relationship("User",back_populates="church")
    detachment=relationship("Detachment",back_populates="church")
    is_active=Column(Boolean,default=True)
    created_at=Column(DateTime,default=datetime.now,onupdate=datetime.now)
    
    