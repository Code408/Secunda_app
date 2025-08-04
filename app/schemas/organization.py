from typing import List, Optional
from pydantic import BaseModel, ConfigDict

class PhoneBase(BaseModel):
    phone: str

class ActivityBase(BaseModel):
    id: int
    name: str
    level: int

    model_config = ConfigDict(from_attributes=True)

class BuildingBase(BaseModel):
    id: int
    address: str
    latitude: float
    longitude: float

    model_config = ConfigDict(from_attributes=True)

class OrganizationBase(BaseModel):
    id: int
    name: str
    phones: List[str]
    building_id: int

    model_config = ConfigDict(from_attributes=True)

# Добавляем схему для вывода с полными связями
class OrganizationOut(OrganizationBase):
    building: BuildingBase
    activities: List[ActivityBase]

class OrganizationCreate(BaseModel):
    name: str
    building_id: int
    phones: List[str]
    activity_ids: List[int]

class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    building_id: Optional[int] = None
    phones: Optional[List[str]] = None
    activity_ids: Optional[List[int]] = None