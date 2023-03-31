from faker import Faker
from apps.schemas.detachment_schemas import DetachmentSchema
fake = Faker()
def test_get_detachments():
    for i in range(30):
        print(fake.name())
 
# 'Lucy Cechtelar'

fake.address()
# '426 Jordy Lodge
#  Cartwrightshire, SC 88120-6700'

fake.text()