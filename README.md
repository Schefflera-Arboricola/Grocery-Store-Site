# About 

It's a 3-user (customer, store manager, delivery executive) e-commerce app to manage a grocery store made using Flask framework and SQLite database. It can be used to search and query products and place orders by customers, manage product inventories and different categories by the store manager, and manage deliveries by the delivery executive. Each folder has a README.md file except static and templates folders. The ScreenFlow folder has screenshots of the website and shows the flow for all three customers. 

<br>

## Features :

1. 3 types of users: Customer, Store Manager, Delivery Executive 
2. CRUD APIs for Product and Category management(flask restful)
3. Proper authentication and authorization framework(flask-login)
4. External APIs: Stripe for online payments, Twilio for OTPs
5. Ability to search Products based on category and various other product features
6. Product recommendation systems for customers based on their previous orders and for showing similar products of a given product based on product description.

<hr>
<br>
<br>

## How to run the code : 

### Running the code:

1. `git clone https://github.com/Schefflera-Arboricola/Grocery-Store.git`
2. `cd Grocery-Store`
3. get API credentials for twilio from [here](https://www.twilio.com/en-us)) and for stripe from [here](https://stripe.com/en-in)

#### using virtual environment :

4. set up your API credentials in `sh local_run.sh` file
5. In `application/config.py` file, in the `LocalDevelopmentConfig` class comment the `SQLITE_DB_DIR` initialisation for docker and uncomment for virtual environment
6. `sh local_setup.sh`
7. `sh local_run.sh`
8. open `http://127.0.0.1:8080` in the browser to view the website

#### using docker :

4. set up your API credentials in `.env` file
5. `docker-compose up --build`
6. open `http://127.0.0.1:8080` in the browser to view the website

*<i>if you get any keyword error, go to inspect and try deleting the cookie data</i>

<br><br>
<hr>

<br>
<br>

Feel free to make any issues/PRs to better the project. 