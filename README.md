## About 

It's a multi-user e-commerce app to manage a grocery store, made using Flask framework and SQLite database. It can be used to search and query products and place orders by customers, manage product inventories and create/edit/delete different categories by the store manager(after approval from the Admin), and manage deliveries by the delivery executive. The developer can use the CRUD APIs for products and categories using their private API keys. Each folder has a README.md file except static and templates folders.

<br>

## Features :

1. 5 types of users: Customer, Admin, Store Manager, Delivery Executive, Developer
2. CRUD APIs for Product and Category management(flask_restx) - You can play around with the API endpoints by pasting the contents of `application/APIdoc.yaml` file in [Swagger Editor](https://editor.swagger.io/)
3. RBAC for authentication and authorization of different user types using flask-login
4. External APIs: Stripe for online payments, Twilio for OTPs
5. Ability to search Products based on category, ratings, and various other product features
6. Product recommendation systems for customers based on their previous orders and for showing similar products of a given product based on product description.
7. Scheduled tasks for sending daily email reminders and monthly reports using flask-mail and Celery. 
8. using flask_caching for caching.


<hr>
<br>

## Functionalities of all user types :

### Customer :
1. Can search products based on category, ratings, and various other product features
2. Can add products to cart and place orders
3. Can view their order history and track their orders
4. Can view their profile and edit their details
5. Can view their recommendations based on their previous orders
6. Can view similar products of a given product based on the product description
7. Can give ratings and reviews to products
8. Can make online payments and receive OTPs for confirmation of delivery
9. Receives daily email reminders and monthly reports based on their activity
10. Can choose whether to receive PDF or text(HTML) monthly reports via email

### Admin :
1. Can view all the store managers' requests for sign-up and approve/reject them
2. Approve/reject requests from store managers to add new categories, edit or delete existing categories
3. Can add/edit/delete products and categories

### Store Manager :
1. Can add/edit/delete products(independently) and categories(needs approval from the Admin)
2. Can view their profile and edit their details
3. Can export all products as a csv file

### Delivery Executive :
1. Can view all the orders assigned to them.
2. Can update the status of the orders(pending/delivered) by entering the OTP received by the customer.
3. Can view their profile and edit their details.

### Developer :
1. Can use the CRUD APIs for products and categories using their private API keys.
2. Can view their profile and edit their details.

<hr>
<br>

## How to run the code : 

### Running the code:

1. `git clone https://github.com/Schefflera-Arboricola/Grocery-Store-Site.git`
2. `cd Grocery-Store-Site`
3. get API credentials for Twilio from [here](https://www.twilio.com/en-us) and for Stripe from [here](https://stripe.com/en-in). For mailing credentials, you might need to generate App password for your Gmail account.
4. set up your API and mail credentials in `.env` file.

#### using virtual environment :

5. `sh local_setup.sh`
6. `sh local_run.sh` 
7. open `http://127.0.0.1:8080` in the browser to view the website

#### WIP - using docker(not recommended, especially if you are a beginner) :

5. In `application/config.py` file, in the `LocalDevelopmentConfig` class un-comment the `SQLITE_DB_DIR` initialization for docker and comment for the virtual environment
6. `docker-compose up --build`
7. open `http://127.0.0.1:8080` in the browser to view the website

<hr>

#### To install Redis on Mac OS :

1. Install Homebrew (if not already installed):
`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
2. Install Redis: `brew install redis`
3. Start the Redis service: `brew services start redis`

<hr>
<br>

### Testing 

1. Test users' login credentials for all types of users : 

- `username` : `aditijuneja`
- `password` : `123456789`

(Change the user's phone number to the number you want to receive the OTP on, using the 'Edit Profile' option on the dashboard)

2. [here](https://stripe.com/docs/testing) you can find some sample cards' credentials for testing payments functionality for Stripe API, for example, 

- `Card number` : `4242 4242 4242 4242`
- `Expiry date` : any future date like `12/34`
- `CVC` : any three-digit CVC
- `zipcode` : any random string of integers

<br>

Feel free to make any issues/PRs to better the project. 


[Old Repository](https://github.com/Schefflera-Arboricola/Grocery-Store)

