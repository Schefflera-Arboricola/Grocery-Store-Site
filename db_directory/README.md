# Description

## Database : 

![db](/static/img/dbdiagram.jpg)

Run the code in `database.dbd` [here](https://dbdiagram.io/) to get the db diagram

<br>

## Data flow :

1. <b>DB Initialisation</b> : Initialisation is done at the end of the `models.py` file, with one branch in `Branch` table, one Admin in `Admin` and 5 Store Manager in `StoreManagerIds` and 10 Delivery Executives in `DeliveryExecutiveIds`. These IDs are required while signing up as store manager and delivery executive. These are provided by the store to them. Category 0 is created for products that are in none of the categories. Store manger cannot delete or edit this category. When a category is deleted, all the products in that category are moved to category 0. The `alembic_version` table was created while performing migration on the db. There is only one Admin allowed in this app and they will approve/reject all the store managers' sign up by verifying their details manually. The admin will also approve/reject the updates purposed by the store managers for categories(stored in `CategoryUpdateRequest`).

2. <b>Placing Orders</b> :

- `Cart` table has all the items currently in the carts of all the customers.
- `OrdersItems` has all the items ordered by all the customers.
- Once the order is placed a new entry is created in the `OrderDetails` table, and the items
in the `Cart` table(for that customer) are transferred to the `OrdersItems` table and the quantities in the `Products` table are also decreased accordingly.
- If payment fails, the order is automatically placed with Cash-on-delivery as the `modeOfPayment`.