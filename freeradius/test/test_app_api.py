import os.path
import sys

import pytest
from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app

client = TestClient(app)

test_numbers_list = ["420735792252|10|10.16.0.19", 
                     "420735792262|11|10.16.0.20",
                     "420735792267|12|10.16.0.21",
                     "420735792266|13|10.16.0.22",
]

test_numbers_dict = [{"username": "420735792252", "id": 10, "ip_address": "10.16.0.19"},
                     {"username": "420735792262", "id": 11, "ip_address": "10.16.0.20"},
                     {"username": "420735792267", "id": 12, "ip_address": "10.16.0.21"},
                     {"username": "420735792266", "id": 13, "ip_address": "10.16.0.22"}
]

def test_tel_number():
    response = client.get("/radius1/tel_number/420735715309")
    assert response.status_code == 200
    assert response.json() == {
        "id": 46,
        "username": "420735715309",
        "value": "10.16.0.55"
    }

@pytest.mark.parametrize("test_numbers", test_numbers_list)
def test_tel_number_from_list_parameters(test_numbers):
    (username, id, ip_address) = test_numbers.split("|")
    response = client.get(f"/radius1/tel_number/{username}")
    assert response.status_code == 200
    assert response.json() == {
        "id": int(id),
        "username": username,
        "value": ip_address
    }

@pytest.mark.parametrize("test_numbers", test_numbers_dict)
def test_tel_number_from_dict_parameters(test_numbers):
    (username, id, ip_address) = (test_numbers["username"], test_numbers["id"], test_numbers["ip_address"])
    response = client.get(f"/radius1/tel_number/{username}")
    assert response.status_code == 200
    assert response.json() == {
        "id": int(id),
        "username": username,
        "value": ip_address
    }

def test_return_ip_addresess():
    response = client.post("/radius1/ip_address/",
                           headers={"X-Token": "hailhydra"},
                           json={"tel_numbers": ["420111222333", "420735715309"]
                           } 
    )    
    assert response.status_code == 200
    assert response.json() == {"420111222333": "10.16.0.67",
                               "420735715309": "10.16.0.55"
    }

def test_return_ip_addresess2():
    temp_dict = {item['username']: item['ip_address'] for item in test_numbers_dict}
    print(temp_dict)
    tel_n = list(temp_dict.keys())
    tel_n_return = {item: temp_dict[item] for item in tel_n}
    response = client.post("/radius1/ip_address/",
                           headers={"X-Token": "hailhydra"},
                           json={"tel_numbers": tel_n
                           } 
    )    
    assert response.status_code == 200
    assert response.json() == tel_n_return

