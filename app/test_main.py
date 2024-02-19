from fastapi.testclient import TestClient
from app.main import app
import pytest

@pytest.fixture(scope='module')
def auth_headers():
    auth_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbjJAZ21haWwuY29tIiwiZXhwIjoxNzA3OTg0MTU5fQ.rpXaPY7X017jZ-g32BpZTVMhDi7cDwAH2dQD35zbkxY"
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

def test_create_infomode(auth_headers):
        payload={
            "Info_Mode":"Infomode_01"
        }
        response=client.post('/info_mode',json=payload,headers=auth_headers)
        assert response.status_code == 200   
def test_update_infomode(auth_headers):
    payload={
        'Info_Mode':"new_infomod"
    } 
    response=client.put('/update_infomode/1',json=payload,headers=auth_headers)  
    print("response_infomode",response.text)   
    assert response.status_code==200    
def test_dlt_infomode(auth_headers):
    response=client.delete('/dlt_infomode/1',headers=auth_headers)
    print("delete_text",response.text)
    assert  response.status_code==200    

def test_complaint(auth_headers):
    payload={ 
   "Complainant_Name":"complaint_01",
   "Mob_Number":"9404300883" , 
   "Email":"mendhe.pravin123@gmail.com",                       
   "Address":"nagpur",
   "Pin_Code":12345,
   "Adhar_Number":"1234567890",
   "Station_id":5,
   "Auth_Person":"pravin_jadhav",
   "Designation_id":3,
   "Place_Occurance":"nagpur",
   "Dfrom_Pstation":"5 km from ps",
   "Relation_Victim":"mother",
   "Mode_Complaint":2,
   "Dutty_Officer":"jadhav",
   "Preliminary_enq_Officer":"pre_jadhav",
   "Investing_Officer":"investigation",
   "Complainant_Imgpath":"image_path" ,
   "Complaint_Desc":"no_desc",
   "user_id":0,
   } 
    response=client.post('/create_complaint',json=payload,headers=auth_headers)  
    print("------------",response.text)  
    assert response.status_code==200
import requests    
def test_form():
    # Create form data
    form_data = {
        "name": "John",
        "last_name": "Doe"
    }

    # Send a POST request with form data
    response = client.post('/test_form', json=form_data)

    # Ensure the response status code is 200 OK
    assert response.status_code == 200

    # Return the response
    return response

def test_crime_method(auth_headers):
    payload={
         "Crime_Type":"crime_type_007",
         "Description":"crime_description"
    }
    response=client.post('/create_crimetype',json=payload,headers=auth_headers)
    print(response.json)
    print('=====',response.text)
    assert response.status_code==200
def test_update_type(auth_headers):
    payload={
        "Crime_Type":"crime_type_04",
         "Description":"crime_description"
    }   
    response=client.put('update_crimetype/4',json=payload)
    print("print==>",response.text)
    assert response.status_code==200 
def test_crime_dlt():
    response=client.delete('/dlt_crimetype/10') 
    print('=========',response.text)
    assert response.status_code==200   
def test_com_accused():
    file = {'image': open("C:/Users/HP LAPTOP/Downloads/2024-01-0205_54_52_632114.png",'rb')}
    data={'com_accused': '{"complaint_id": 2, "Accused_Name": "pravin mendhe", "Aliase": "dada", "Accused_Age": 12, "Accused_Address": "nagpur", "relation":"mother", "Remark": "pravin", "Accused_Imgpath":}'}
    response=client.put('/update_comaccused/1',data=data)
    print("com_accused_test",response.text)
    assert response.status_code==200
      
    




