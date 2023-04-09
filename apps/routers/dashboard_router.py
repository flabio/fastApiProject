from fastapi import APIRouter,Depends,status
from apps.config.db import get_db
from sqlalchemy.orm  import Session 
from apps.repository.dashboard_repository import DashboardRepository
from apps.auth import check_comandant

dashboard_router=APIRouter(
    prefix="/api/v1/dashboard",
    tags=["dashboard"]
)

@dashboard_router.get("/", dependencies=[Depends(check_comandant)],status_code=status.HTTP_200_OK)
async def counts_scouts(db:Session=Depends(get_db)):
    return await DashboardRepository.counts_scouts(db)
    