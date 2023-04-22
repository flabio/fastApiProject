from fastapi.testclient import TestClient
import sys 
import os
from faker import Faker
fake = Faker()

sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
from main import app
from apps.model.user_model import User
cliente =TestClient(app)

def test_crear_scout():
    user=User()
    #   "first_name": fake.name(),
    #         "last_name": fake.last_name()+" "+fake.last_name_nonbinary(),
    #         "identification": fake.isbn10(),
    #         "type_identification": "Nuip",
    #         "expedition_date": "2023-23-12",
    #         "birth_day": "2014-03-15",
    #         "birth_place": "bogota",
    #         "gender": "M",
    #         "rh": "O+",
    #         "direction": fake.address(),

    #         "cell_phone": fake.phone_number(),
    #         "civil_status": "free union",

    #         "occupation": "test",
    #         "school": 2,
    #         "grade": 2,

    #         "baptism_water": True,
    #         "baptism_spirit": True,
    #         "is_active":True,
    #         "email": fake.email(),

    #         "rol_id": 13,
    #         "church_id": 2,
    #         "city_id": 1,
    #         "sub_detachment_id": 2,
    #         "eps_name": "Nueva Eps",
    #         "department_name": "Cumdinamarca",
    #         "location_name": "Engativa",


    #     }
    for i in range(100):
        # user={
        #     "first_name": fake.name(),
        #     "last_name": fake.last_name()+" "+fake.last_name_nonbinary(),
        #     "identification": fake.isbn10(),
        #     "type_identification": "Nuip",
        #     "expedition_date": "2023-23-12",
        #     "birth_day": "2014-03-15",
        #     "birth_place": "bogota",
        #     "gender": "M",
        #     "rh": "O+",
        #     "direction": fake.address(),
        #     "cell_phone": fake.phone_number(),
        #     "civil_status": "free union",
        #     "occupation": "test",
        #     "school": 2,
        #     "grade": 2,
        #     "baptism_water": True,
        #     "baptism_spirit": True,
        #     "is_active":True,
        #     "email": fake.email(),
        #     "rol_id": 13,
        #     "church_id": 2,
        #     "city_id": 1,
        #     "sub_detachment_id": 2,
        #     "eps_name": "Nueva Eps",
        #     "department_name": "Cumdinamarca",
        #     "location_name": "Engativa",


        # }
        user={
        
        "first_name":fake.name(),
        "last_name":fake.last_name()+" "+fake.last_name_nonbinary(),
        "identification": fake.isbn10(),
        "type_identification":"Nuip",
        "birth_day":"2016-03-15",
        "rh":"O+",
        "direction":fake.address(),
        "cell_phone":fake.phone_number(),
        "grade":2,  
        "school_name":fake.company(),
        "eps_name":fake.company(),
        "department_name":"Cumdinamarca",
        "location_name":"Engativa",
        "city_id":1,
        "church_id":7,
        "sub_detachment_id":1,
        "rol_id":13,
        "email":fake.email(),
        "ceated_at":"2022-11-11"
          }
        
        response=cliente.post('/api/v1/scout/',json=user)
        #assert response.status_code ==201
        print(response,"status",response.text)
        # print("*"*20)
        # print(response.json())
    pass