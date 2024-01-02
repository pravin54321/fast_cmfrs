from fastapi.testclient import TestClient
from app.main import app
import pytest

@pytest.fixture(scope='module')
def auth_headers():
    auth_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJwcmF2aW4iLCJleHAiOjE3MDQxODEzNzF9.DlooXmaBKN-gEco806nP1Ze5i6lEYHSjVlfKzMamAcA"
    return{
         "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
client = TestClient(app)

def test_create_designation_with_token(auth_headers):
   
    payload = {"Designation": "Engineer_08"}
    response = client.post("/designation_created", json=payload, headers=auth_headers)
    assert response.status_code == 200
    duplicate_data={"Designation":'Engineer_08'}
    response=client.post('/designation_created',json=duplicate_data,headers=auth_headers)
    assert response.status_code==400
    assert "duplicate" in response.text.lower()
def test_update_designation(auth_headers):
    update_data = {'Designation': 'Engineer_01_02'}  
    # Ensure the URL starts with a slash and includes the designation ID
    response = client.put('/update_designation/2', json=update_data, headers=auth_headers)
    assert response.status_code == 200
def test_get_all_designation(auth_headers):
    response=client.get('/get_designation',headers=auth_headers)
    assert response.status_code==200
    assert isinstance(response.json(),list)  
def test_delete_designation(auth_headers):
    designation_id = 3  # Replace with the ID you want to delete
    url = f'/del_designation/{designation_id}'
    
    # Print or log information about the request before sending it
    print("Request URL:", url)
    print("Headers:", auth_headers)
    
    response = client.delete(url, headers=auth_headers)
    
    # Print or log the response for inspection
    print("Response status code:", response.status_code)
    print("Response body:", response.text)
    
    assert response.status_code == 200 