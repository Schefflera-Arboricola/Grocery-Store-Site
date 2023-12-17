from application.models import *
from ML_models.similarProducts import *

# based on past orders : most recent orders and more frequently bought orders are given more importance

# todo : caching
# todo : recommendation with some weight to avg_rating 

def recommendProducts(products, categories, orderItems):
    rprod = []
    d = {}
    for item in orderItems:
        product = getProducts([item["product_id"],], products)[0]
        sim_products = similarProducts(product, products, categories)
        for i in sim_products:
            i = i["product_id"]
            if i not in d:
                d[i] = 1
            else:
                d[i] += 1
    for i in sorted(d, key=d.get, reverse=True):
        prod = getProducts([i,], products)[0]
        rprod.append(prod)
    return rprod
