# Description

1. `views` : 

        - `auth.py`: contains all the routes for sign in, signup, signout, forgot password
        - `viewsCustomer.py`: contains all the routes for the customer
        - `viewsDelExe.py`: contains all the routes for delivery executive
        - `viewsStoreMng.py`: contains all the routes for the store manager
        - `viewsDeveloper.py`: contains all the routes for the developer

2. How to use API? (for 'developer' account_type only) :

   - get the API credentials from the developer dashboard
   - paste the contents of `APIdoc.yaml` file in [Swagger Editor](https://editor.swagger.io/) and play with APIs in swagger editor
   - Or run the following in a new terminal window(while the app is running in back) :

        `curl -X GET 'http://127.0.0.1:8080/api/{endpoint}' -H 'Authorization: Bearer YOUR_API_KEY'` <br>
         or <br>
        ```
        curl -X POST 'http://127.0.0.1:8080/api/{endpoint}' \
        -H 'Authorization: Bearer YOUR_API_KEY' \
        -H 'Content-Type: application/json' \
        -d '{
            "field1": "value1",
            "field2": "value2"
        }'
        ```