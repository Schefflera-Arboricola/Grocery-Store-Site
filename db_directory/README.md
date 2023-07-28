# Description

## Database : 

![db](/static/img/db.jpg)

<br>

## Data flow :

1. Database is initialized with one branch in Branch table and one Store Manager in StoreManagerIds and three Delivery Executives in DeliveryExecutiveIds. These IDs are required while signing up as store manager and delivery executive.
2. Cart table has all the items currently in the carts of all the customers.
3. OrdersItems has all the items ordered by all the customers.
4. Once the order is placed a new entry is created in the OrderDetails table, and the items
in the Cart table(for that customer) are transferred to the OrdersItems table and the quantities in the Products table are also decreased using the API.
5. If payment fails, the order is automatically placed with Cash-on-delivery as the mode of payment.