# About 

It's a 3-user (customer, store manager, delivery executive) e-commerce app to manage a grocery store made using Flask framework and SQLite database. It can be used to search and query products and place orders by customers, manage product inventories and different categories by the store manager, and manage deliveries by the delivery executive. Each folder has a README.md file except static and templates folders.

<br>

## how to run the code : 

### Before running the code:

1. Have the following installed :
    - Python 3.5 or later versions
    - Git
    - venv or virtualenv installed on system to create and manage virtual environments
    - DB browser for SQLite
    - C Compiler (For Some Python Libraries such as numpy and scikit-learn)
    - Internet access for external APIs
2. Have accounts on [stripe](https://stripe.com/en-in) and [twilio](https://www.twilio.com/en-us) to generate API keys. If you will be using a trail account for otp, then set the trail number as the customer's number to get the OTP.


### Running the code:

1. `git clone https://github.com/Schefflera-Arboricola/Grocery-Store.git`
2. `cd Grocery-Store`
3. In `application/config.py` add your `account_sid` , `auth_token` and `sender_phone` for sending OTPs(generate API key from [here](https://www.twilio.com/en-us)) 
4. In `main.py` add your `app.config['STRIPE_PUBLIC_KEY']` and `app.config['STRIPE_SECRET_KEY']` for online payments(generate API key from [here](https://stripe.com/en-in))
5. `sh local_setup.sh`
6. `sh local_run.sh`
7. open `http://127.0.0.1:8080` in browser to view the website
(if it gives account_type keyword error, go to inscpect and delete cookie session data in Application in storage in cookie in http://127.0.0.1:8080 then right click and click on delete token and session)

<br><br>
<hr>

<h2>Features :</h2>

1. 3 types of users : Customer, Store Manager, Delivery Executive 
2. CRUD APIs for Product and Category management(flask restful)
3. Proper authentication and authorisation framework(flask-login)
4. External APIs : Stripe for online payments, Twilio for OTPs
5. Ability to search Products based on category and various other product features
6. Product recommendation systems for customers based on their previous orders and for showing similar products of a given product based on product description.

<hr>

<br>
<br>

Around 20 initial commits are not very well documented. Feel free to make any issues/PRs to better the project. 