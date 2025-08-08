from sqlalchemy import Column, Integer, String, JSON, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.models import Base

class Organization(Base):
    __tablename__ = 'organizations'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    building_id = Column(Integer, ForeignKey('buildings.id'), nullable=False)
    phones = Column(JSON)  # Список телефонов: ["+7-XXX-XXX-XX-XX"]
    
    building = relationship("Building", back_populates="organizations")
    activities = relationship("Activity", secondary="organization_activities")

# Ассоциативная таблица для связи многие-ко-многим
organization_activities = Table(
    'organization_activities',
    Base.metadata,
    Column('organization_id', Integer, ForeignKey('organizations.id'), primary_key=True),
    Column('activity_id', Integer, ForeignKey('activities.id'), primary_key=True)
)