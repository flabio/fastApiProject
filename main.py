from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from apps.routers.auth_router import auth_router
from apps.routers.user_router import router
from apps.routers.study_conducted_router import study_conducted_router
from apps.routers.city_router import city_router
from apps.routers.rol_router import rol_router
from apps.routers.church_router import church_router
from apps.routers.detachment_router import detachment_router
from apps.routers.sub_detachment_router import sub_detachment_router
from apps.routers.ministerial_academy_router import ministerial_academy_router
from apps.routers.scout_router import scout_router
from apps.routers.parentesco_router import parentesco_router
import uvicorn
from apps.config.db import Base,engine

def create_tables():
    Base.metadata.create_all(bind=engine)

create_tables()

app=FastAPI()
origins = ["*"]



app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static",StaticFiles(directory="static"),name="static")
app.include_router(auth_router)
app.include_router(city_router)
app.include_router(rol_router)
app.include_router(church_router)
app.include_router(detachment_router)
app.include_router(sub_detachment_router)
app.include_router(router)
app.include_router(ministerial_academy_router)
app.include_router(study_conducted_router)
app.include_router(scout_router)
app.include_router(parentesco_router)
if __name__ == "__main__":
    uvicorn.run("main:app",reload=True)

# alembic revision --autogenerate -m "Create models"
# alembic upgrade heads