import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from application.models import *

# based on product and category description, category desc given more importance

# todo : caching

def similarProducts(given_product, products, categories, N=6):
    # N : maximum number of similar products to be returned

    product_ids = []
    product_descriptions = []

    for product in products:
        product_ids.append(product["product_id"])
        product_description = (
            2 * product["name"]
            + " "
            + 2 * getCategoryDesc(product["category_id"], categories)
            + " "
            + product["description"]
        )
        product_descriptions.append(product_description)

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(product_descriptions)

    given_product_description = (
        2 * given_product["name"]
        + " "
        + 2 * getCategoryDesc(given_product["category_id"], categories)
        + " "
        + given_product["description"]
    )
    given_product_tfidf = vectorizer.transform([given_product_description])
    cos_sim_scores = cosine_similarity(given_product_tfidf, tfidf_matrix)

    sorted_indices = np.argsort(cos_sim_scores[0])[::-1]

    sorted_indices = sorted_indices[1:]

    similar_product_ids = [product_ids[idx] for idx in sorted_indices[:N]]

    similar_products = getProducts(similar_product_ids, products)

    return similar_products


def getCategoryDesc(category_id, categories):
    for category in categories:
        if category["category_id"] == category_id:
            return category["description"]
    else:
        raise Exception("Category not found. Contact Admin.")


def getProducts(product_ids, products):
    product_list = []
    for product_id in product_ids:
        for product in products:
            if product["product_id"] == product_id:
                product_list.append(product)
                break
    return product_list
