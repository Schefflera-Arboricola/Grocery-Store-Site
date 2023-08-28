'''
Test flow : 

- create app
- create client and get token, for each API endpoint and test it
'''

from bs4 import BeautifulSoup
from ..conftests import app

app_instance=app()

def get_test_developer_info():
    developer_id=1
    username='aditijuneja'
    password='123456789'
    return developer_id,username,password


def get_client_and_token(app_instance):
    client = app_instance.test_client()
    dev_id,username,password=get_test_developer_info()
    with app_instance.app_context():
        response = client.post('/', data={'username': username, 'password': password})
        assert response.status_code == 200

        response=client.get(f'/developer/{dev_id}/getAPI')
        assert response.status_code == 200

        html_content = response.data.decode('utf-8')
        soup = BeautifulSoup(html_content, 'html.parser')
        target_div = soup.find('div', {'id': 'API_key'})
        if target_div:
            token = target_div.get_text(strip=True)
        else:
            raise Exception("No API key found")
    
    return client, token



# GET requests
def test_get_all_products(app_instance):
    client,token=get_client_and_token(app_instance)
    with app_instance.app_context():
        headers = {'Authorization': f'Bearer {token}'}
        response = client.get('/api/products', headers=headers)
        assert response.status_code == 200
    return
'''
def test_get_one_product(app):
    client,token=get_client_and_token(app)
    test_product=create_test_product(app,client,token)
    headers = {'Authorization': f'Bearer {token}'}
    response = client.get(f'/api/products/{test_product}', headers=headers)
    assert response.status_code == 200
    delete_test_product(app,client,token,test_product)
    return
    
def test_get_all_products_in_category(app):
    client,token=get_client_and_token(app)
    headers = {'Authorization': f'Bearer {token}'}
    response = client.get('/api/products/1/0', headers=headers) #using category 0 instead of making a test category and filling it with test products
    assert response.status_code == 200    
    return

def test_get_all_categories(app):
    client,token=get_client_and_token(app)
    headers = {'Authorization': f'Bearer {token}'}
    response = client.get('/api/categories', headers=headers)
    assert response.status_code == 200
    return

def test_get_one_category(app):
    client,token=get_client_and_token(app)
    headers = {'Authorization': f'Bearer {token}'}
    response = client.get(f'/api/categories/0', headers=headers) #using category 0 instead of making a test category
    assert response.status_code == 200
    return



# POST and DELETE requests
def test_post_and_delete_product(app):
    client,token=get_client_and_token(app)
    test_product=create_test_product(app,client,token)
    delete_test_product(app,client,token,test_product)
    return

def test_post_and_delete_category(app):
    client,token=get_client_and_token(app)
    test_category=create_test_category(app,client,token)
    delete_test_category(app,client,token,test_category)
    return



# PUT requests
def test_put_product(app):
    client,token=get_client_and_token(app)
    test_product=create_test_product(app,client,token)
    data ={
            "name": "test1",
            "description": "test1",
            "price": 1,
            "quantity": 1,
            "unit": "test1",
            "pricePerUnit": 1,
            "category_id": 1,
            "manufacture_date": "01-01-0002",
            "expiry_date": "01-01-0003",
            "image_url": "test1",
            "avg_rating": 1
        }
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    response = client.put(f'/api/products/{test_product}', headers=headers, data=data)
    assert response.status_code == 201
    delete_test_product(app,client,token,test_product)
    return

def test_put_category(app):
    client,token=get_client_and_token(app)
    test_category=create_test_category(app,client,token)
    data={
        "name": "test1",
        "description": "test1"
    }
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    response = client.put(f'/api/categories/{test_category}', headers=headers, data=data)
    assert response.status_code == 201
    delete_test_category(app,client,token,test_category)
    return



# Helper functions
def create_test_product(app,client,token):
    data ={
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
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    response = client.post('/api/products', headers=headers, data=data)
    assert response.status_code == 201
    return response.json['product_id']

def delete_test_product(app,client,token,product_id):
    headers = {'Authorization': f'Bearer {token}'}
    response = client.delete(f'/api/products/{product_id}', headers=headers)
    assert response.status_code == 200
    return

def create_test_category(app,client,token):
    data={
        "name": "test",
        "description": "test"
    }
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    response = client.post('/api/categories', headers=headers, data=data)
    assert response.status_code == 201
    return response.json['category_id']

def delete_test_category(app,client,token,category_id):
    headers = {'Authorization': f'Bearer {token}'}
    response = client.delete(f'/api/categories/{category_id}', headers=headers)
    assert response.status_code == 200
    return
'''