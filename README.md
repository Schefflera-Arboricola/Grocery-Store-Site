## About 

It's a multi-user e-commerce app to manage a grocery store, made using Flask framework and SQLite database. It can be used to search and query products and place orders by customers, manage product inventories and create/edit/delete different categories by the store manager(after the approval from the Admin), and manage deliveries by the delivery executive. The developer can use the CRUD APIs for products and categories using their private API keys. Each folder has a README.md file except static and templates folders. The ScreenFlow folder has screenshots of the website and shows the flow for all users(except developer). 

<br>

## Features :

1. 5 types of users: Customer, Admin, Store Manager, Delivery Executive, Developer
2. CRUD APIs for Product and Category management(flask_restx) - You can play around with the API endpoints by pasting the contents of `application/APIdoc.yaml` file in [Swagger Editor](https://editor.swagger.io/)
3. Proper authentication and authorization framework(flask-login)
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
6. Can view similar products of a given product based on product description
7. Can give ratings and reviews to products
8. Can make online payments and receive OTPs for confirmation of delivery
9. Receives daily email reminders and monthly reports
10. Can choose whether to receive pdf or text monthly reports via email

### Admin :
1. Can view all the store managers' requests for sign up and approve/reject them
2. Approve/reject requests from store managers to add new categories, edit or delete existing categories
3. Can add/edit/delete products and categories

### Store Manager :
1. Can add/edit/delete products(independently) and categories(needs approval from the Admin)
2. Can view their profile and edit their details
3. Can export all products as a csv file

### Delivery Executive :
1. Can view all the orders assigned to them.
2. Can update the status of the orders(pending/delivered) by entring the OTP received by the customer.
3. Can view their profile and edit their details.

### Developer :
1. Can use the CRUD APIs for products and categories using their private API keys.
2. Can view their profile and edit their details.

<hr>
<br>

## How to run the code : 

### Running the code:

1. `git clone https://github.com/Schefflera-Arboricola/Grocery-Store.git`
2. `cd Grocery-Store`
3. get API credentials for Twilio from [here](https://www.twilio.com/en-us) and for Stripe from [here](https://stripe.com/en-in)

#### using virtual environment :

4. set up your API and mail credentials in `sh local_run.sh` file.(for mailing credentials you might need to generate App password for your Gmail account)
5. In `application/config.py` file, in the `LocalDevelopmentConfig` class comment the `SQLITE_DB_DIR` initialization for docker and uncomment for the virtual environment
6. `sh local_setup.sh`
7. `sh local_run.sh`
8. open `http://127.0.0.1:8080` in the browser to view the website

#### using docker :

4. set up your API credentials in `.env` file
5. `docker-compose up --build`
6. open `http://127.0.0.1:8080` in the browser to view the website

*<i> If you get any keyword error, go to inspect and try deleting the cookie data</i>

<hr>

#### To install Redis on Mac OS :

1. Install Homebrew (if not already installed):
`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
2. Install Redis: `brew install redis`
3. Start the Redis service: `brew services start redis`

<hr>
<br>

## No DB on this branch :

Test users' login credentials for all types of users : 

- `username` : `aditijuneja`
- `password` : `123456789`

(Change the user's phone number to the number you want to receive the OTP on, using the 'Edit Profile' option on the dashboard)

<br>

Feel free to make any issues/PRs to better the project. 


[Old Repository](https://github.com/Schefflera-Arboricola/Grocery-Store)

## ToDos :

1. fix Docker image of this branch
2. Configure tests properly
3. issues in workflow
