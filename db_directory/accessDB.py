from application.models import *
import sqlite3


def GetDailyMailCustomers():
    """Returns a list of dictionary having customer details
    for customers who have not logged in for more than 24hrs
    and whose last_login=None"""

    conn = sqlite3.connect("db_directory/gs.sqlite3")
    cursor = conn.cursor()

    query = """
        SELECT email FROM Customer
        WHERE last_login IS NULL OR last_login < date('now', '-1 day')
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    c = []
    for row in rows:
        c += [row[0]]
    cursor.close()
    conn.close()

    return c


def GetMonthlyMailCustomers(month):
    conn = sqlite3.connect("db_directory/gs.sqlite3")
    cursor = conn.cursor()

    query = f"""
        SELECT od.customer_id, c.customer_id, c.name, c.email, c.username, c.report_format
        FROM order_details od
        JOIN Customer c ON od.customer_id = c.customer_id
        WHERE strftime('%m', od.order_date) = '{month:02}'
    """

    cursor.execute(query)

    rows = cursor.fetchall()

    unique_customers = []
    customer_ids = set()
    for row in rows:
        if row[0] not in customer_ids:
            customer = {
                "customer_id": row[0],
                "name": row[2],
                "email": row[3],
                "username": row[4],
                "report_format": row[5],
            }
            unique_customers.append(customer)
            customer_ids.add(row[0])

    cursor.close()
    conn.close()
    return unique_customers


def GetMonthlyReport(customer_id, month):
    def get_total(orders):
        total_amount = 0
        for order in orders:
            total_amount += order["total_price"]
        return total_amount

    conn = sqlite3.connect("db_directory/gs.sqlite3")
    cursor = conn.cursor()

    query_orders = f"""
        SELECT od.order_id, od.delivery_status, od.order_date, od.total_price,
            oi.quantity, oi.price, p.name
        FROM order_details od
        JOIN orders_items oi ON od.order_id = oi.order_id
        JOIN Products p ON oi.product_id = p.product_id
        WHERE strftime('%m', od.order_date) = ? AND od.customer_id = ?
    """

    cursor.execute(query_orders, (f"{month:02}", customer_id))
    rows = cursor.fetchall()

    customer_orders = []
    for row in rows:
        order_exists = any(o["order_id"] == row[0] for o in customer_orders)
        if not order_exists:
            order = {
                "order_id": row[0],
                "delivery_status": row[1],
                "order_date": row[2],
                "total_price": row[3],
                "order_details": [],
            }
            customer_orders.append(order)

        for order_dict in customer_orders:
            if order_dict["order_id"] == row[0]:
                order_dict["order_details"].append(
                    {"quantity": row[4], "price": row[5], "product_name": row[6]}
                )

    total = get_total(customer_orders)

    cursor.close()
    conn.close()

    return customer_orders, total


def GetCategory(category_id=None):
    if category_id:
        category = Category.query.get(category_id)
        if category:
            return (
                {
                    "category_id": category.category_id,
                    "name": category.name,
                    "description": category.description,
                },
                200,
            )
        else:
            return {"message": "Category not found"}, 404
    else:
        categories = Category.query.all()
        results = [
            {
                "category_id": category.category_id,
                "name": category.name,
                "description": category.description,
            }
            for category in categories
        ]
        return results, 200


def AddCategory(data):
    name = data["name"]
    description = data["description"]
    if type(name) != str:
        return {"message": "Name must be a string"}, 404
    elif Category.query.filter_by(name=name).first():
        return {"message": f"{name} already exists"}, 404
    else:
        category = Category(name=name, description=description)
        db.session.add(category)
        db.session.commit()
        return {"message": "Category created successfully"}, 200


def UpdateCategory(category_id, data):
    category = Category.query.get(category_id)
    if category:
        name = data["name"]
        description = data["description"]
        if type(name) != str:
            return {"message": "Name must be a string"}, 404
        else:
            category.name = name
            category.description = description
            db.session.add(category)
            db.session.commit()
            return {"message": "Category updated successfully"}, 200
    else:
        return {"message": "Category not found"}, 404


def DeleteCategory(category_id):
    category = Category.query.get(category_id)
    if category:
        # Update products associated with the category
        products = Products.query.filter_by(category_id=category_id).all()
        for product in products:
            product.category_id = 0  # Set category_id to 0
            db.session.add(product)
        db.session.delete(category)
        db.session.commit()
        return (
            {
                "message": "Category deleted successfully.  Associated products are in category 0 now."
            },
            200,
        )
    else:
        return {"message": "Category not found"}, 404


def GetProduct(product_id=None, flag=0, category_id=None):
    if flag == 0:
        if product_id:
            product = Products.query.get(product_id)
            if product:
                if product.isDeleted != "True":
                    return (
                        {
                            "product_id": product.product_id,
                            "name": product.name,
                            "description": product.description,
                            "price": product.price,
                            "quantity": product.quantity,
                            "unit": product.unit,
                            "pricePerUnit": product.pricePerUnit,
                            "category_id": product.category_id,
                            "manufacture_date": product.manufacture_date,
                            "expiry_date": product.expiry_date,
                            "image_url": product.image_url,
                            "avg_rating": product.avg_rating,
                        },
                        200,
                    )
                else:
                    return {"message": "Product was deleted"}, 404
            else:
                return {"message": "Product not found"}, 404
        else:
            products = Products.query.all()
            results = [
                {
                    "product_id": product.product_id,
                    "name": product.name,
                    "description": product.description,
                    "price": product.price,
                    "quantity": product.quantity,
                    "unit": product.unit,
                    "pricePerUnit": product.pricePerUnit,
                    "category_id": product.category_id,
                    "manufacture_date": product.manufacture_date,
                    "expiry_date": product.expiry_date,
                    "image_url": product.image_url,
                    "avg_rating": product.avg_rating,
                }
                for product in products
                if product.isDeleted != "True"
            ]
            return results, 200
    if flag == 1:
        category = Category.query.get(category_id)
        if category:
            products = Products.query.filter_by(category_id=category_id).all()
            results = [
                {
                    "product_id": product.product_id,
                    "name": product.name,
                    "description": product.description,
                    "price": product.price,
                    "quantity": product.quantity,
                    "unit": product.unit,
                    "pricePerUnit": product.pricePerUnit,
                    "category_id": product.category_id,
                    "manufacture_date": product.manufacture_date,
                    "expiry_date": product.expiry_date,
                    "image_url": product.image_url,
                    "avg_rating": product.avg_rating,
                }
                for product in products
                if product.isDeleted != "True"
            ]
            return results, 200
        else:
            return {"message": "Category not found"}, 404
    else:
        return {"message": "Error!! Contact Admin"}, 404


def AddProduct(data):
    name = data["name"]
    description = data["description"]
    price = data["price"]
    quantity = data["quantity"]
    unit = data["unit"]
    pricePerUnit = data["pricePerUnit"]
    category_id = data["category_id"]
    manufacture_date = data["manufacture_date"]
    expiry_date = data["expiry_date"]
    image_url = data["image_url"]
    avg_rating = None
    isDeleted = "False"

    product_msg, status = check_product(
        name,
        description,
        price,
        quantity,
        unit,
        pricePerUnit,
        category_id,
        manufacture_date,
        expiry_date,
        image_url,
        avg_rating,
    )
    if status == True:
        product = Products(
            name=name,
            description=description,
            price=float(price),
            quantity=int(quantity),
            unit=unit,
            pricePerUnit=float(pricePerUnit),
            category_id=int(category_id),
            manufacture_date=manufacture_date,
            expiry_date=expiry_date,
            image_url=image_url,
            avg_rating=avg_rating,
            isDeleted=isDeleted,
        )
        db.session.add(product)
        db.session.commit()
        return {"message": "Product created successfully"}, 200
    elif status == False:
        return {"message": product_msg}, 404
    else:
        return {"message": "Something went wrong!! Contact admin"}, 404


def UpdateProduct(product_id, data):
    product = Products.query.get(product_id)
    if product:
        name = data["name"]
        description = data["description"]
        price = data["price"]
        quantity = data["quantity"]
        unit = data["unit"]
        pricePerUnit = data["pricePerUnit"]
        category_id = data["category_id"]
        manufacture_date = data["manufacture_date"]
        expiry_date = data["expiry_date"]
        image_url = data["image_url"]
        avg_rating = data["avg_rating"]
        isDeleted = "False"

        product_msg, status = check_product(
            name,
            description,
            price,
            quantity,
            unit,
            pricePerUnit,
            category_id,
            manufacture_date,
            expiry_date,
            image_url,
            avg_rating,
        )
        if status == True:
            product.name = name
            product.description = description
            product.price = float(price)
            product.quantity = int(quantity)
            product.unit = unit
            product.pricePerUnit = float(pricePerUnit)
            product.category_id = int(category_id)
            product.manufacture_date = manufacture_date
            product.expiry_date = expiry_date
            product.image_url = image_url
            product.avg_rating = avg_rating
            product.isDeleted = isDeleted
            db.session.commit()
            return {"message": "Product updated successfully"}, 200
        elif status == False:
            return {"message": product_msg}, 404
        else:
            return {"message": "Error!! Contact Admin"}, 404
    else:
        return {"message": "Product not found"}, 404


def DeleteProduct(product_id):
    product = Products.query.get(product_id)
    if product:
        product.isDeleted = "True"
        db.session.commit()
        return {"message": "Product deleted successfully"}, 200
    else:
        return {"message": "Product not found"}, 404


def check_product(
    name,
    description,
    price,
    quantity,
    unit,
    pricePerUnit,
    category_id,
    manufacture_date,
    expiry_date,
    image_url,
    avg_rating,
):
    if type(name) != str:
        return "Name must be a string", False
    elif type(description) != str:
        return "Description must be a string", False
    elif type(unit) != str:
        return "Unit must be a string", False
    elif not Category.query.get(category_id):
        return "Invalid category_id", False
    elif type(image_url) != str:
        return "Image_url must be a string", False
    elif float(price) < 0:
        return "Price cannot be negative", False
    elif float(quantity) < 0:
        return "Quantity cannot be negative", False
    elif float(pricePerUnit) < 0:
        return "PricePerUnit cannot be negative", False
    else:
        return "Valid", True
