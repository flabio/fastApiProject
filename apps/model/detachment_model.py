from apps.config.db import Base
from sqlalchemy import Column,Boolean,Integer,String,DateTime
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class Detachment(Base):
    __tablename__ = 'detachment'
    id = Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String)
    section = Column(String(20))
    numbers=Column(Integer)
    district=Column(String(20))
    church_id=Column(Integer,ForeignKey("church.id",ondelete="CASCADE"),nullable=False)
    church=relationship("Church",back_populates="detachment")
    is_active=Column(Boolean,default=True)
    created_at=Column(DateTime,default=datetime.now,onupdate=datetime.now)
