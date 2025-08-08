import math
from typing import List, Optional
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.organization import Organization
from app.models.activity import Activity
from app.models.building import Building
from app.schemas.organization import (
    OrganizationBase,
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationOut
)

class OrganizationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id: int) -> Optional[OrganizationOut]:
        result = await self.db.execute(
            select(Organization)
            .options(
                joinedload(Organization.building),
                joinedload(Organization.activities)
            )
            .where(Organization.id == id)
        )
        return result.scalars().first()

    async def get_by_building(self, building_id: int) -> List[OrganizationOut]:
        result = await self.db.execute(
            select(Organization)
            .options(
                selectinload(Organization.building),
                selectinload(Organization.activities)
            )
            .where(Organization.building_id == building_id)
        )
        return result.unique().scalars().all()

    async def get_by_activity(self, activity_id: int) -> List[OrganizationBase]:
        result = await self.db.execute(
            select(Organization)
            .join(Organization.activities)
            .where(Activity.id == activity_id)
        )
        return result.unique().scalars().all()

    async def get_by_activity_tree(self, activity_id: int):
        # получаешь все дочерние activity_id...
        all_ids = await self._get_all_descendant_ids(activity_id)

        result = await self.db.execute(
            select(Organization)
            .join(Organization.activities)
            .options(
                selectinload(Organization.building),
                selectinload(Organization.activities)
            )
            .where(Activity.id.in_(all_ids))
        )
        return result.unique().scalars().all()

    async def _get_all_descendant_ids(self, activity_id: int) -> List[int]:
        """Get all descendants up to 3 levels deep, including root"""
        result = await self.db.execute(
            select(Activity).where(Activity.level <= 3)
        )
        all_activities = result.scalars().all()

        # Построим дерево в памяти
        children_map = {}
        for activity in all_activities:
            children_map.setdefault(activity.parent_id, []).append(activity)

        ids = []
        stack = [activity_id]
        while stack:
            current_id = stack.pop()
            ids.append(current_id)
            for child in children_map.get(current_id, []):
                stack.append(child.id)

        return ids

    async def search_by_name(self, name: str) -> List[OrganizationOut]:
        result = await self.db.execute(
            select(Organization)
            .options(
                joinedload(Organization.building),  # или selectinload
                joinedload(Organization.activities)
            )
            .where(Organization.name.ilike(f"%{name}%"))
        )
        return result.unique().scalars().all()

    async def create(self, data: OrganizationCreate) -> Organization:
        org = Organization(
            name=data.name,
            building_id=data.building_id,
            phones=data.phones
        )

        result = await self.db.execute(
            select(Activity).where(Activity.id.in_(data.activity_ids))
        )
        activities = result.scalars().all()
        org.activities = activities

        self.db.add(org)
        await self.db.commit()
        await self.db.refresh(org)
        return org

    async def update(self, id: int, data: OrganizationUpdate) -> Optional[Organization]:
        result = await self.db.execute(
            select(Organization).where(Organization.id == id)
        )
        org = result.scalars().first()
        if not org:
            return None

        if data.name:
            org.name = data.name
        if data.building_id:
            org.building_id = data.building_id
        if data.phones:
            org.phones = data.phones
        if data.activity_ids:
            result = await self.db.execute(
                select(Activity).where(Activity.id.in_(data.activity_ids))
            )
            org.activities = result.scalars().all()

        await self.db.commit()
        await self.db.refresh(org)
        return org

    async def delete(self, id: int) -> bool:
        result = await self.db.execute(
            select(Organization).where(Organization.id == id)
        )
        org = result.scalars().first()
        if not org:
            return False

        await self.db.delete(org)
        await self.db.commit()
        return True

    async def get_nearby(self, lat: float, lon: float, radius: float) -> List[OrganizationOut]:
        earth_radius = 6371  # in kilometers
        max_lat = lat + (radius / earth_radius) * (180 / math.pi)
        min_lat = lat - (radius / earth_radius) * (180 / math.pi)
        max_lon = lon + (radius / earth_radius) * (180 / math.pi) / math.cos(lat * math.pi / 180)
        min_lon = lon - (radius / earth_radius) * (180 / math.pi) / math.cos(lat * math.pi / 180)

        result = await self.db.execute(
            select(Organization)
            .options(
                joinedload(Organization.building),
                joinedload(Organization.activities)
            )
            .join(Building)
            .where(
                Building.latitude.between(min_lat, max_lat),
                Building.longitude.between(min_lon, max_lon)
            )
        )
        return result.unique().scalars().all()

    async def get_all_activities(self) -> List[Activity]:
        result = await self.db.execute(
            select(Activity)
        )
        return result.scalars().all()
    
    async def get_all_buildings(self) -> List[Building]:
        result = await self.db.execute(
            select(Building)
        )
        return result.scalars().all()
    
    async def get_all(self) -> List[OrganizationOut]:
        print(">>> get_all() called")
        result = await self.db.execute(
            select(Organization).options(
                joinedload(Organization.building),
                joinedload(Organization.activities)
            )
        )
        return result.unique().scalars().all()
