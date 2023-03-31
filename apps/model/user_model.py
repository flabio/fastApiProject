from apps.config.db import Base
from sqlalchemy import Column, Integer,Boolean, String,DateTime,Text
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True,autoincrement=True)
    image=Column(String)
    first_name=Column(String)
    last_name=Column(String)
    identification=Column(String)
    type_identification=Column(String(10))
    birth_day=Column(String(12))
    birth_place=Column(Text)
    expedition_date=Column(String)
    gender=Column(String(10))
    rh=Column(String(6))
    direction=Column(String(50))
    phone_number=Column(String)
    cell_phone=Column(String)
    civil_status=Column(String)
    position=Column(String)
    occupation=Column(String)
    school_name=Column(String)
    school=Column(Integer)
    eps_name=Column(Text)
    grade=Column(Integer)
    hobbies_interests=Column(Text)
    allergies=Column(Text)
    department_name=Column(Text)
    location_name=Column(Text)
    baptism_water=Column(Boolean,default=False)
    baptism_spirit=Column(Boolean,default=False)
    year_conversion=Column(Integer)
    email=Column(String,unique=True)
    username=Column(String)
    password=Column(String)
    rol_id=Column(Integer,ForeignKey("rol.id",ondelete="CASCADE"))
    rol = relationship("Rol",back_populates="user")
    church_id=Column(Integer,ForeignKey("church.id",ondelete="CASCADE"),nullable=False)
    church=relationship("Church",back_populates="user")
    city_id=Column(Integer,ForeignKey("city.id",ondelete="CASCADE"),nullable=False)
    city=relationship("City",back_populates="user")
    sub_detachment_id=Column(Integer,ForeignKey("subdetachment.id",ondelete="CASCADE"),nullable=True)
    ceated_at=Column(DateTime,default=datetime.now,onupdate=datetime.now)
    is_active=Column(Boolean,default=True)    
    #ministerial_academy_user = relationship("MinisterialAcademyUser", back_populates="user")
    
    
 		     
	          
