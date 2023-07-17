from flask import request
from flask_restful import Resource
from application.database import db
from application.models import Category, Products

class CategoryAPI(Resource):
    def get(self, category_id=None):
        if category_id:
            category = Category.query.get(category_id)
            if category:
                return {
                    'category_id': category.category_id,
                    'name': category.name,
                    'description': category.description
                }, 200
            else:
                return {'message': 'Category not found'}, 404
        else:
            categories = Category.query.all()
            results = [
                {
                    'category_id': category.category_id,
                    'name': category.name,
                    'description': category.description
                }
                for category in categories
            ]
            return results, 200

    def post(self):
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        if type(name)!=str  :return {'message': 'Name must be a string'}, 404
        elif Category.query.filter_by(name=name).first(): return {'message': f'{name} already exists'}, 404
        else:
            category = Category(name=name, description=description)
            db.session.add(category)
            db.session.commit()
            return {'message': 'Category created successfully'}, 201

    def put(self, category_id):
        category = Category.query.get(category_id)
        if category:
            data = request.get_json()
            name = data.get('name')
            description = data.get('description')
            if type(name)!=str  :return {'message': 'Name must be a string'}, 404
            else:
                category.name=name
                category.description=description
                db.session.add(category)
                db.session.commit()
                return {'message': 'Category updated successfully'}, 201
        else:
            return {'message': 'Category not found'}, 404


    def delete(self, category_id):
        category = Category.query.get(category_id)
        if category:
            # Update products associated with the category
            products = Products.query.filter_by(category_id=category_id).all()
            for product in products:
                product.category_id = None  # Set category_id to NULL
                db.session.add(product)
            db.session.delete(category)
            db.session.commit()
            return {'message': 'Category deleted successfully.  Associated products don\'t have a category anymore!'}, 200
        else:
            return {'message': 'Category not found'}, 404
        


class ProductAPI(Resource):
    def get(self, product_id=None,flag=0,category_id=None):
        if flag==0:
            if product_id:
                product = Products.query.get(product_id)
                if product:
                    return {
                        'product_id': product.product_id,
                        'name': product.name,
                        'description': product.description,
                        'price': product.price,
                        'quantity': product.quantity,
                        'unit': product.unit,
                        'pricePerUnit': product.pricePerUnit,
                        'category_id': product.category_id,
                        'manufacture_date': product.manufacture_date,
                        'expiry_date': product.expiry_date,
                        'image_url': product.image_url,
                        'avg_rating': product.avg_rating
                    }, 200
                else:
                    return {'message': 'Product not found'}, 404
            else:
                products = Products.query.all()
                results = [
                    {
                        'product_id': product.product_id,
                        'name': product.name,
                        'description': product.description,
                        'price': product.price,
                        'quantity': product.quantity,
                        'unit': product.unit,
                        'pricePerUnit': product.pricePerUnit,
                        'category_id': product.category_id,
                        'manufacture_date': product.manufacture_date,
                        'expiry_date': product.expiry_date,
                        'image_url': product.image_url,
                        'avg_rating': product.avg_rating
                    }
                    for product in products
                ]
                return results, 200
        if flag==1:
            category = Category.query.get(category_id)
            if category:
                products = Products.query.filter_by(category_id=category_id).all()
                results = [
                    {
                        'product_id': product.product_id,
                        'name': product.name,
                        'description': product.description,
                        'price': product.price,
                        'quantity': product.quantity,
                        'unit': product.unit,
                        'pricePerUnit': product.pricePerUnit,
                        'category_id': product.category_id,
                        'manufacture_date': product.manufacture_date,
                        'expiry_date': product.expiry_date,
                        'image_url': product.image_url,
                        'avg_rating': product.avg_rating
                    }
                    for product in products
                ]
                return results, 200
            else:
                return {'message': 'Category not found'}, 404
        else:
            return {'message': 'flag=0'}, 404

    def post(self):
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        price = data.get('price')
        quantity = data.get('quantity')
        unit = data.get('unit')
        pricePerUnit = data.get('pricePerUnit')
        category_id = data.get('category_id')
        manufacture_date = data.get('manufacture_date')
        expiry_date = data.get('expiry_date')
        image_url = data.get('image_url')
        avg_rating= data.get('avg_rating')
        
        product_msg, status = check_product(name, description, price, quantity, unit, pricePerUnit, category_id, manufacture_date, expiry_date, image_url,avg_rating)
        if status==200:
            product = Products(name=name,description=description,price=float(price),quantity=int(quantity),unit=unit,pricePerUnit=float(pricePerUnit),category_id=int(category_id),manufacture_date=manufacture_date,expiry_date=expiry_date,image_url=image_url,avg_rating=avg_rating)
            db.session.add(product)
            db.session.commit()
            return {'message': 'Product created successfully'}, 201
        elif status==400:
            return {'message': product_msg}, 404
        else:
            return {'message': 'Something went wrong!! Contact admin'}, 404
        

    def put(self, product_id):
        product = Products.query.get(product_id)
        if product:
            data = request.get_json()
            name = data.get('name')
            description = data.get('description')
            price = data.get('price')
            quantity = data.get('quantity')
            unit = data.get('unit')
            pricePerUnit = data.get('pricePerUnit')
            category_id = data.get('category_id')
            manufacture_date = data.get('manufacture_date')
            expiry_date = data.get('expiry_date')
            image_url = data.get('image_url')
            avg_rating= data.get('avg_rating')

            product_msg, status = check_product(name, description, price, quantity, unit, pricePerUnit, category_id, manufacture_date, expiry_date, image_url,avg_rating)
            if status==200:
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
                product.avg_rating=avg_rating
                db.session.commit()
                return {'message': 'Product updated successfully'}, 201
            elif status==400:
                return {'message': product_msg}, 404
            else:
                return {'message': 'Error!! Contact Admin'}, 404
        else:
            return {'message': 'Product not found'}, 404

    def delete(self, product_id):
        product = Products.query.get(product_id)
        if product:
            db.session.delete(product)
            db.session.commit()
            return {'message': 'Product deleted successfully'}, 200
        else:
            return {'message': 'Product not found'}, 404


def check_product(name, description, price, quantity, unit, pricePerUnit, category_id, manufacture_date, expiry_date, image_url,avg_rating):
    if type(name)!=str:
        return 'Name must be a string', 400
    elif type(description)!=str:
        return 'Description must be a string', 400
    elif type(unit)!=str:
        return 'Unit must be a string', 400
    elif not Category.query.get(category_id):    
        return 'Invalid category_id', 400
    elif type(image_url)!=str:
        return 'Image_url must be a string', 400
    else:
        return 'Valid', 200