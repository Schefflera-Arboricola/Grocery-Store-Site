'''
- create a store manager client
- use category 0 as test category
- create a test product in the test category

- create a customer client
- search based on test category
- add to cart the test product
- checkout with CoD

- create a delivery executive client
- check if the order is there

- use store manager client
- check if the test product's quantity decreased
- delete the test product 
'''

#from application.models import *
from bs4 import BeautifulSoup
import pytest
from main import create_app

@pytest.fixture
def app():
    app, api = create_app()
    return app

def get_test_store_manager_info():
    store_manager_id=1
    username='aditi'
    password='123456789'
    return store_manager_id,username,password

def get_test_customer_info():
    customer_id=1
    username='aditi'
    password='123456789'
    return customer_id,username,password

def get_test_delivery_executive_info():
    delivery_executive_id=1
    username='aditi'
    password='123456789'
    return delivery_executive_id,username,password

def test_place_order(app):
    client = app.test_client()
    store_manager_id,username,password=get_test_store_manager_info()
    response = client.post('/', data={'username': username, 'password': password})
    assert response.status_code == 200
    
    data={
        "name": "test",
        "description": "test",
        "price": 0,
        "quantity": 0,
        "unit": "test",
        "pricePerUnit": 0,
        "category_id": 0,
        "manufacture_date": "01-01-0001",
        "expiry_date": "01-01-0002",
        "image_url": "test"
    }
    #response=client.get(f'/storemng/{store_manager_id}/addProducts',data=data)
    #assert response.status_code == 201
    return 

