from fastapi.testclient import TestClient
from app.main import app
import pytest

@pytest.fixture(scope='module')
def auth_headers():
    auth_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbjJAZ21haWwuY29tIiwiZXhwIjoxNzA3NzE4Mzk4fQ.OOXoh9oevQJ0NDPjbS7AADwqYrFJ6YG5ce7OALTCjwI"
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

#----------------testing_user_logine----------------------
def test_stationlogin(auth_headers):
    payload={
        "PoliceStation_id":"6",
        "Email":"admin3@gmail.com",
        "Password":"123",
        "Designation_id":"4",
        "User_Name":"pravin_03",
        "Mob_Number":"9158380283"
        } 
    response=client.post('policestation_login',json=payload,headers=auth_headers)
    print('Response body',response.text) 
    assert response.status_code==200  
def test_updstationlogin(auth_headers):
    payload={
        "PoliceStation_id":"5",
        "Email":"admin4@gmail.com",
        "Password":"123",
        "Designation_id":"4",
        "User_Name":"pravin_03",
        "Mob_Number":"9404300883"
        } 
    response=client.patch('/update_policelogine/2',json=payload,headers=auth_headers)
    print("responsebody",response.text)
    assert response.status_code==200
def test_getstationlogin(auth_headers):
    response=client.get("/get_station_login",headers=auth_headers)
    print('response body',response.json())
    assert response.status_code==200    
def test_delstation_login(auth_headers):
    response=client.delete('/del_stationlog/1',headers=auth_headers)
    print("response body",response.text)
    assert response.status_code==200
def test_create_post(auth_headers):
    payload={
  "Post": "post_04",
  "State_id": 5,
  "Region_id": 4,
  "Distric_id": 4,
  "HeadOffice_id": 4,
  "Subdivision_id": 4,
  "Taluka_id": 4,
  "PoliceStation_id": 4
  }
    response=client.post('/create_post',json=payload,headers=auth_headers)
    print("response_text",response.text)
    assert response.status_code==200 
def test_dlt_state(auth_headers):
    response=client.delete('/delete_state/5',headers=auth_headers)
    print("=========",response.text)
    assert response.status_code==200
        
   

    




