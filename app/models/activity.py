from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models import Base

class Activity(Base):
    __tablename__ = 'activities'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)  # Укажите длину строки (например, 255)
    parent_id = Column(Integer, ForeignKey('activities.id'), nullable=True)
    level = Column(Integer, nullable=False)  # 1, 2 или 3
    
    children = relationship("Activity", back_populates="parent")
    parent = relationship("Activity", remote_side=[id], back_populates="children")