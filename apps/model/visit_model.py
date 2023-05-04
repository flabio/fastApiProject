from apps.config.db import Base
from sqlalchemy import Column, Integer,Boolean, String,DateTime,Text
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


class Visit(Base):
    __tablename__ = 'visit'
    id = Column(Integer, primary_key=True,autoincrement=True)
    visit_date=Column(String)
    visit_description=Column(Text)
    visit_status=Column(String)
    user_id=Column(Integer,ForeignKey("user.id",ondelete="CASCADE"),nullable=True)
    sub_detachment_id=Column(Integer,ForeignKey("subdetachment.id",ondelete="CASCADE"),nullable=True)
    ceated_at=Column(DateTime,default=datetime.now,onupdate=datetime.now)
    is_active=Column(Boolean,default=True)    

    
    
 		     
	          
