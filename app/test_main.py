from fastapi.testclient import TestClient
from app.main import app
import pytest

@pytest.fixture(scope='module')
def auth_headers():
    auth_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbjJAZ21haWwuY29tIiwiZXhwIjoxNzA5MjA5MDk4fQ.Y5cS2sKjWIlwKzYSM5y0NQcuwriaeOKeIhZ7AcmB3qc"
    return{
         "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
client = TestClient(app)
def test_create_State(auth_headers):
    payload={"State":'Keral'}
    response=client.post('/state',json=payload,headers=auth_headers)
    if response.status_code==400:
        print(response.text)
    assert response.status_code==200
def test_update_state(auth_headers):
    payload={"State":"updated_test"}
    respnse=client.put('/update_state/4',json=payload,headers=auth_headers)
    if respnse.status_code==400:
        print(respnse.text)
    assert respnse.status_code==200
def test_get_state(auth_headers):
    response=client.get('/get_state',headers=auth_headers)
    assert response.status_code==200
def test_delete_state(auth_headers):
    response=client.delete('/delete_state/6',headers=auth_headers)
    assert response.status_code==200   
#--------------------------region---------------------------------------
# def test_create_regione    
             

