from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from app.services.organization import OrganizationService
from app.schemas.organization import OrganizationOut
from app.db.session import get_db

# Создаем основной роутер
router = APIRouter(prefix="/api/v1")

@router.get("/organizations/{id}", response_model=OrganizationOut)
def get_organization(id: int, db: Session = Depends(get_db)):
    return OrganizationService(db).get_by_id(id)

@router.get("/organizations/", response_model=list[OrganizationOut])
def get_organizations(
    building_id: int = Query(None),
    activity_id: int = Query(None),
    name: str = Query(None),
    db: Session = Depends(get_db)
):
    service = OrganizationService(db)
    if building_id:
        return service.get_by_building(building_id)
    if activity_id:
        return service.get_by_activity(activity_id)
    if name:
        return service.search_by_name(name)
    return []