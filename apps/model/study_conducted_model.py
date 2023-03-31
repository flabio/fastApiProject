from apps.config.db import Base
from sqlalchemy import Column,Integer,Text,Boolean,DateTime
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


class StudyConducted(Base):
    __tablename__='study_conducted'
    id = Column(Integer,primary_key=True,autoincrement=True,nullable=True)
    title_obtained=Column(Text)
    semestre_numbre=Column(Integer)
    user_id=Column(Integer,ForeignKey("user.id",ondelete="CASCADE"))
    is_active = Column(Boolean,default=True)
    created_at=Column(DateTime,default=datetime.now,onupdate=datetime.now)
    

class StudyGraduate(Base):
    __tablename__='study_graduate'
    id = Column(Integer,primary_key=True,autoincrement=True,nullable=True)
    title_obtained=Column(Text)
    type_name=Column(Text)
    user_id=Column(Integer,ForeignKey("user.id",ondelete="CASCADE"))
    is_active = Column(Boolean,default=True)
    created_at=Column(DateTime,default=datetime.now,onupdate=datetime.now)