from apps.config.db import Base
from sqlalchemy import Column,Integer,String,Text,Boolean,DateTime

from sqlalchemy.orm import relationship
from datetime import datetime

class MinisterialAcademy(Base):
    __tablename__='ministerial_academy'
    id = Column(Integer,primary_key=True,autoincrement=True,nullable=True)
    name=Column(Text)
    is_active = Column(Boolean,default=True)
    #ministerial_academy_user = relationship("ministerial_academy_user", back_populates="ministerial_academy")
    created_at=Column(DateTime,default=datetime.now,onupdate=datetime.now)
    
    