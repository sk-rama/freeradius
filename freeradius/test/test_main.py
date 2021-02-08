import os.path
import sys
from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app

client = TestClient(app)

def test_tel_number():
    response = client.get("/radius1/tel_number/420735715309")
    assert response.status_code == 200
    assert response.json() == {
        "id": 46,
        "username": "420735715309",
        "value": "10.16.0.55"
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

