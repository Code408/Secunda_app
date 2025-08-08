from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models import Base
from sqlalchemy import event
from sqlalchemy.orm import validates

class Activity(Base):
    __tablename__ = 'activities'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    parent_id = Column(Integer, ForeignKey('activities.id'), nullable=True)
    level = Column(Integer, nullable=False)  # 1, 2 или 3
    
    children = relationship("Activity", back_populates="parent")
    parent = relationship("Activity", remote_side=[id], back_populates="children")

    @validates('parent_id')
    def validate_parent(self, key, parent_id):
        if parent_id:
            parent = self.__class__.query.get(parent_id)
            if parent.level >= 3:
                raise ValueError("Maximum hierarchy depth is 3 levels")
            self.level = parent.level + 1
        else:
            self.level = 1
        return parent_id

@event.listens_for(Activity, 'before_insert')
@event.listens_for(Activity, 'before_update')
def validate_activity_level(mapper, connection, target):
    if target.level < 1 or target.level > 3:
        raise ValueError("Activity level must be between 1 and 3")
