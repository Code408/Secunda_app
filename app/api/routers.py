from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from typing import List, Optional

from app.services.organization import OrganizationService
from app.schemas.organization import OrganizationOut
from app.db.session import get_db

router = APIRouter(prefix="/api/v1")
templates = Jinja2Templates(directory="app/templates")

# API Endpoints
@router.get("/organizations/{id}", response_model=OrganizationOut,
            summary="Get organization by ID",
            description="Returns full organization details by its ID")
async def get_organization(id: int, db: AsyncSession = Depends(get_db)):
    return await OrganizationService(db).get_by_id(id)

@router.get("/organizations/", response_model=List[OrganizationOut],
            summary="List organizations",
            description="Returns filtered list of organizations")
async def get_organizations(
    building_id: Optional[int] = Query(None, description="Building ID filter"),
    activity_id: Optional[int] = Query(None, description="Activity ID filter (includes child activities)"), 
    name: Optional[str] = Query(None, description="Partial name search"),
    db: AsyncSession = Depends(get_db)
):
    service = OrganizationService(db)
    if building_id:
        return await service.get_by_building(building_id)
    if activity_id:
        return await service.get_by_activity_tree(activity_id)
    if name:
        return await service.search_by_name(name)
    return await service.get_all()

@router.get("/organizations/nearby/", response_model=List[OrganizationOut],
            summary="Nearby organizations",
            description="Returns organizations within given radius from location")
async def get_nearby_organizations(
    lat: float = Query(..., description="Latitude of center point"),
    lon: float = Query(..., description="Longitude of center point"),
    radius: float = Query(1.0, description="Search radius in kilometers"),
    db: AsyncSession = Depends(get_db)
):
    return await OrganizationService(db).get_nearby(lat, lon, radius)

# Web Interface Endpoints
@router.get("/web/organizations/", include_in_schema=False)
async def web_organizations(
    request: Request,
    building_id: Optional[int] = None,
    activity_id: Optional[int] = None,
    name: Optional[str] = None,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    radius: float = 1.0,
    db: AsyncSession = Depends(get_db)
):
    service = OrganizationService(db)
    organizations = []
    
    if building_id:
        organizations = await service.get_by_building(building_id)
    elif activity_id:
        organizations = await service.get_by_activity_tree(activity_id)
    elif name:
        organizations = await service.search_by_name(name)
    elif lat is not None and lon is not None:
        organizations = await service.get_nearby(lat, lon, radius)

    return templates.TemplateResponse(
        "organizations/list.html",
        {
            "request": request,
            "organizations": jsonable_encoder(organizations),
            "buildings": await service.get_all_buildings(),
            "activities": await service.get_all_activities(),
            "search_params": {
                "building_id": building_id,
                "activity_id": activity_id,
                "name": name,
                "lat": lat,
                "lon": lon,
                "radius": radius
            }
        }
    )
@router.get("/web/organizations/{id}", response_model=OrganizationOut, include_in_schema=False)
async def get_organization(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db)
):
    service = OrganizationService(db)
    organization = await service.get_by_id(id)
    return templates.TemplateResponse(
        "organizations/detail.html",
        {
            "request": request,
            "organization": organization
        }
    )