from flask import request
from flask_restx import Resource
from application.database import db
from application.models import Category, Products
from flask_jwt_extended import jwt_required
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import current_app as app
from datetime import datetime

limiter = Limiter(key_func=get_remote_address)


class CategoryAPI(Resource):
    @jwt_required()
    @limiter.limit("100 per hour")
    def get(self, category_id=None):
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

    @jwt_required()
    @limiter.limit("100 per hour")
    def post(self):
        data = request.get_json()
        name = data.get("name")
        description = data.get("description")
        if type(name) != str:
            return {"message": "Name must be a string"}, 400
        elif Category.query.filter_by(name=name).first():
            return {"message": f"{name} already exists"}, 404
        else:
            category = Category(name=name, description=description)
            db.session.add(category)
            db.session.commit()
            category_id = category.category_id
            return (
                {
                    "message": "Category created successfully",
                    "category_id": category_id,
                },
                201,
            )

    @jwt_required()
    @limiter.limit("100 per hour")
    def put(self, category_id):
        category = Category.query.get(category_id)
        if category:
            data = request.get_json()
            name = data.get("name")
            description = data.get("description")
            if type(name) != str:
                return {"message": "Name must be a string"}, 400
            else:
                category.name = name
                category.description = description
                db.session.add(category)
                db.session.commit()
                return {"message": "Category updated successfully"}, 201
        else:
            return {"message": "Category not found"}, 404

    @jwt_required()
    @limiter.limit("100 per hour")
    def delete(self, category_id):
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
                    "message": "Category deleted successfully.  Associated products have category 0 now"
                },
                200,
            )
        else:
            return {"message": "Category not found"}, 404


class ProductAPI(Resource):
    @jwt_required()
    @limiter.limit("100 per hour")
    def get(self, product_id=None, flag=0, category_id=None):
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
                        return {"message": "Product was deleted"}, 400
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
            return {"message": "flag=0"}, 400

    @jwt_required()
    @limiter.limit("100 per hour")
    def post(self):
        data = request.get_json()
        name = data.get("name")
        description = data.get("description")
        price = data.get("price")
        quantity = data.get("quantity")
        unit = data.get("unit")
        pricePerUnit = data.get("pricePerUnit")
        category_id = data.get("category_id")
        manufacture_date = data.get("manufacture_date")
        expiry_date = data.get("expiry_date")
        image_url = data.get("image_url")
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
        if status == 200:
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
            product_id = product.product_id
            return (
                {"message": "Product created successfully", "product_id": product_id},
                201,
            )
        elif status == 400:
            return {"message": product_msg}, 400
        else:
            return {"message": "Something went wrong!! Contact admin"}, 500

    @jwt_required()
    @limiter.limit("100 per hour")
    def put(self, product_id):
        product = Products.query.get(product_id)
        if product:
            data = request.get_json()
            name = data.get("name")
            description = data.get("description")
            price = data.get("price")
            quantity = data.get("quantity")
            unit = data.get("unit")
            pricePerUnit = data.get("pricePerUnit")
            category_id = data.get("category_id")
            manufacture_date = data.get("manufacture_date")
            expiry_date = data.get("expiry_date")
            image_url = data.get("image_url")
            avg_rating = data.get("avg_rating")
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
            if status == 200:
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
                return {"message": "Product updated successfully"}, 201
            elif status == 400:
                return {"message": product_msg}, 400
            else:
                return {"message": "Error!! Contact Admin"}, 500
        else:
            return {"message": "Product not found"}, 404

    @jwt_required()
    @limiter.limit("100 per hour")
    def delete(self, product_id):
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
        return "Name must be a string", 400
    elif type(description) != str:
        return "Description must be a string", 400
    elif type(unit) != str:
        return "Unit must be a string", 400
    elif not Category.query.get(category_id):
        return "Invalid category_id", 400
    elif type(image_url) != str:
        return "Image_url must be a string", 400
    elif float(price) < 0:
        return "Price cannot be negative", 400
    elif float(quantity) < 0:
        return "Quantity cannot be negative", 400
    elif float(pricePerUnit) < 0:
        return "PricePerUnit cannot be negative", 400
    elif avg_rating != None and (float(avg_rating) < 0 or float(avg_rating) > 5):
        return "Avg_rating must be between 0 and 5", 400
    elif not is_valid_date(manufacture_date):
        return "manufacture_date is not a valid date.", 400
    elif not is_valid_date(expiry_date):
        return "expiry_date is not a valid date.", 400
    elif datetime.strptime(manufacture_date, "%d-%m-%Y") > datetime.strptime(
        expiry_date, "%d-%m-%Y"
    ):
        return "Manufacture_date cannot be greater than expiry_date", 400
    else:
        return "Valid", 200


def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%d-%m-%Y")
        return True
    except ValueError:
        return False
