from fastapi import APIRouter,Depends,status
from apps.config.db import get_db
from sqlalchemy.orm  import Session 
from apps.repository.dashboard_repository import DashboardRepository
from apps.auth import check_comandant
from typing import Optional
dashboard_router=APIRouter(
    prefix="/api/v1/dashboard",
    tags=["dashboard"]
)

@dashboard_router.get("/", dependencies=[Depends(check_comandant)],status_code=status.HTTP_200_OK)
async def counts_scouts(church_id:Optional[int],year:Optional[int],db:Session=Depends(get_db)):
    return await DashboardRepository.counts_scouts(church_id,year,db)

@dashboard_router.get("/chart_by_year_scouts",status_code=status.HTTP_200_OK)
async def chart_by_year_scouts(church_id:Optional[int],year:Optional[int],db:Session=Depends(get_db)):
    return await DashboardRepository.chart_by_year_scouts(church_id,year,db)

@dashboard_router.get("/chart_church__scouts",status_code=status.HTTP_200_OK)
async def chart_church__scouts(church_id:Optional[int],year:Optional[int],db:Session=Depends(get_db)):
    return await DashboardRepository.chart_church__scouts(church_id,year,db)

