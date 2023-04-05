from apps.config.db import Base
from sqlalchemy import Column, Integer,Boolean, String,DateTime,Text
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class Parentesco(Base):
    __tablename__ = 'parentesco'
    id = Column(Integer, primary_key=True,autoincrement=True)
    first_name=Column(String)
    last_name=Column(String)
    identification=Column(String)
    type_parentesco=Column(String(10))
    direction=Column(String(50))
    cell_phone=Column(String)
    civil_status=Column(String)
    is_active=Column(Boolean,default=True)    
    ceated_at=Column(DateTime,default=datetime.now,onupdate=datetime.now)
    
    
 		     
	          
