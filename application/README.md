# Description

1. `views` : 

        - `auth.py`: contains all the routes for sign in, signup, signout, forgot password
        - `viewsCustomer.py`: contains all the routes for the customer
        - `viewsDelExe.py`: contains all the routes for delivery executive
        - `viewsStoreMng.py`: contains all the routes for the store manager
        - `viewsDeveloper.py`: contains all the routes for the developer

2. How to use API? (for developers only) :

<ol>
    <li>get the API credentials from the dashboard</li>
    <li>run this in a new terminal window :

`curl -X GET 'http://127.0.0.1:8080/{endpoint}' -H 'Authorization: Bearer YOUR_API_KEY'` <br>
or
```
curl -X POST 'http://127.0.0.1:8080/{endpoint}' \
-H 'Authorization: Bearer YOUR_API_KEY' \
-H 'Content-Type: application/json' \
-d '{
    "field1": "value1",
    "field2": "value2"
}'
```
</li>
</ol>
</div>

3. `api.py` endpoints :

        - Categories
   
            - `GET` : 
                - `/categories`: returns a list of all categories
                    ```
                    [{
                        'category_id': 1,
                        'name': <category.name>,
                        'description': <category.description>
                    },
                    {
                        'category_id': 2,
                        'name': <category.name>,
                        'description': <category.description> 
                    }
                    .....
                    ] , 200
                    ```
                - `/categories/<category_id>` : returns all the attributes of the category with the given category_id
                    ```
                    {
                        'category_id': category.category_id,
                        'name': category.name,
                        'description': category.description
                    }, 200
                ``` 
            - `POST` :
                - `/categories` : creates a new category `{'message': 'Category created successfully'}, 201`
            - `PUT` :
                - `/categories/<category_id>` : updates the category with the given category_id `{'message': 'Category updated successfully'}, 201`
            - `DELETE` :
                - `/categories/<category_id>` : deletes the category with the given category_id `{'message': 'Category deleted successfully.  Associated products don\'t have a category anymore!'}, 200`              


       - Products
            - `GET` :
                - `/products` : returns a list of all products
                    ```
                    [
                        {
                            'product_id': product.product_id,
                            'name': product.name,
                            'description': product.description,
                            'price': product.price,
                            'quantity': product.quantity,
                            'unit': product.unit,
                            'pricePerUnit': product.pricePerUnit,
                            'category_id': product.category_id,
                            'manufacture_date': product.manufacture_date,
                            'expiry_date': product.expiry_date,
                            'image_url': product.image_url,
                            'avg_rating': product.avg_rating
                        },...
                    ], 200
                    ```
                - `/products/<product_id>` : returns all the attributes of the product with the given product_id
                    ```
                    {
                        'product_id': product.product_id,
                        'name': product.name,
                        'description': product.description,
                        'price': product.price,
                        'quantity': product.quantity,
                        'unit': product.unit,
                        'pricePerUnit': product.pricePerUnit,
                        'category_id': product.category_id,
                        'manufacture_date': product.manufacture_date,
                        'expiry_date': product.expiry_date,
                        'image_url': product.image_url,
                        'avg_rating': product.avg_rating
                    }, 200
                    ```
                - `/products/<flag>/<category_id>` : returns a list of all products with the given category_id
                    ```
                    [
                        {
                            'product_id': product.product_id,
                            'name': product.name,
                            'description': product.description,
                            'price': product.price,
                            'quantity': product.quantity,
                            'unit': product.unit,
                            'pricePerUnit': product.pricePerUnit,
                            'category_id': product.category_id,
                            'manufacture_date': product.manufacture_date,
                            'expiry_date': product.expiry_date,
                            'image_url': product.image_url,
                            'avg_rating': product.avg_rating
                        },...
                    ], 200
                    ```
            - `POST` :
                - `/products` : creates a new product `{'message': 'Product created successfully'}, 201`
            - `PUT` :
                - `/products/<product_id>` : updates the product with the given product_id `{'message': 'Product updated successfully'}, 201`
            - `DELETE` :
                - `/products/<product_id>` : deletes the product with the given product_id `{'message': 'Product deleted successfully'}, 200`
