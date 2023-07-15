how to run the code : 

1. `git clone https://github.com/Schefflera-Arboricola/Grocery-Store.git`
2. `cd Grocery-Store`
3. In `application/config.py` add your `account_sid` , `auth_token` and `sender_phone` for sending OTPs(generate API key from [here](https://www.twilio.com/en-us)) 
4. In `main.py` add your `app.config['STRIPE_PUBLIC_KEY']` and `app.config['STRIPE_SECRET_KEY']` for online payments(generate API key from [here](https://stripe.com/en-in))
5. `sh local_setup.sh`
6. `sh local_run.sh`

<br><br>

<h2>Database : </h2>

![db](/static/img/db.jpg)

<br>

<h2>Some points about the DB :</h2>

1. Database is initialized with one branch in Branch table and one Store Manager in StoreManagerIds and three Delivery Executives in DeliveryExecutiveIds. These IDs are required while signing up as store manager and delivery executive.
2. Cart table has all the items currently in the carts of all the customers.
3. OrdersItems has all the items ordered by all the customers.
4. Once the order is placed a new entry is created in the OrderDetails table, and the items
in the Cart table(for that customer) are transferred to the OrdersItems table and the quantities in the Products table are also decreased using the API.
5. If payment fails, the order is automatically placed with Cash-on-delivery as the mode of payment.
<br>

<h2>Features :</h2>

1. 3 types of users : Customer, Store Manager, Delivery Executive 
2. CRUD APIs for Product and Category management
3. Proper signin-signup framework made using flask-login
4. Validations before adding the data in database
5. Ability to search Products based on category and various product features
6. Ability to add products to cart and place orders
<br>

<br>
<br>

Around 20 initial commits are not very well documented.