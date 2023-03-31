
from fastapi.testclient import TestClient

from apps.routers.detachment_router import detachment_router
from faker import Faker

from .main import app
fake = Faker()



client = TestClient(app)
# detachment_router=APIRouter(
#     prefix="/api/v1/detachment",
#     tags=["detachment"],
# )

def test_get_detachments():
    
    for i in range(30):
        print(fake.name())
   

# alembic revision --autogenerate -m "Create models"
# alembic upgrade heads