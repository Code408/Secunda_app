from typing import List
from sqlalchemy.orm import Session, joinedload
from app.models.organization import Organization
from app.schemas.organization import OrganizationOut
from app.models.activity import Activity
from app.models.building import Building
from app.schemas.organization import (
    OrganizationBase,
    OrganizationCreate,
    OrganizationUpdate
)

class OrganizationService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id: int) -> OrganizationOut:
        return (
            self.db.query(Organization)
            .options(
                joinedload(Organization.building),
                joinedload(Organization.activities)
            )
            .filter(Organization.id == id)
            .first()
        )

    def get_by_building(self, building_id: int) -> List[OrganizationBase]:
        return (
            self.db.query(Organization)
            .filter(Organization.building_id == building_id)
            .all()
        )

    def get_by_activity(self, activity_id: int) -> List[OrganizationBase]:
        return (
            self.db.query(Organization)
            .join(Organization.activities)
            .filter(Activity.id == activity_id)
            .all()
        )

    def get_by_activity_tree(self, activity_id: int) -> List[OrganizationBase]:
        activity_ids = self._get_child_activity_ids(activity_id)
        return (
            self.db.query(Organization)
            .join(Organization.activities)
            .filter(Activity.id.in_(activity_ids))
            .all()
        )

    def _get_child_activity_ids(self, activity_id: int) -> List[int]:
        activity = self.db.get(Activity, activity_id)
        if not activity:
            return []
        
        ids = [activity_id]
        for child in activity.children:
            if child.level <= 3:
                ids.extend(self._get_child_activity_ids(child.id))
        return ids

    def search_by_name(self, name: str) -> List[OrganizationBase]:
        return (
            self.db.query(Organization)
            .filter(Organization.name.ilike(f"%{name}%"))
            .all()
        )

    def create(self, data: OrganizationCreate) -> Organization:
        org = Organization(
            name=data.name,
            building_id=data.building_id,
            phones=data.phones
        )
        activities = self.db.query(Activity).filter(Activity.id.in_(data.activity_ids)).all()
        org.activities = activities
        
        self.db.add(org)
        self.db.commit()
        self.db.refresh(org)
        return org

    def update(self, id: int, data: OrganizationUpdate) -> Organization:
        org = self.get_by_id(id)
        if not org:
            return None
            
        if data.name:
            org.name = data.name
        if data.building_id:
            org.building_id = data.building_id
        if data.phones:
            org.phones = data.phones
        if data.activity_ids:
            activities = self.db.query(Activity).filter(Activity.id.in_(data.activity_ids)).all()
            org.activities = activities
            
        self.db.commit()
        self.db.refresh(org)
        return org

    def delete(self, id: int) -> bool:
        org = self.get_by_id(id)
        if not org:
            return False
            
        self.db.delete(org)
        self.db.commit()
        return True