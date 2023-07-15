import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from application.models import *

def similarProducts(given_product, products, categories):
    # Initialize lists to store product ids and their descriptions
    product_ids = []
    product_descriptions = []

    # Collect product descriptions
    for product in products:
        product_ids.append(product['product_id'])
        product_description = product['name'] + getCategoryDesc(product['category_id'], categories) + ' ' + product['description']
        product_descriptions.append(product_description)

    # Create a TF-IDF vectorizer and fit it on the product descriptions
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(product_descriptions)

    # Calculate cosine similarity between the given product and all other products
    given_product_description = given_product['name'] + getCategoryDesc(given_product['category_id'], categories) + ' ' + given_product['description']
    given_product_tfidf = vectorizer.transform([given_product_description])
    cos_sim_scores = cosine_similarity(given_product_tfidf, tfidf_matrix)

    # Get the indices of the products sorted by their similarity scores (descending order)
    sorted_indices = np.argsort(cos_sim_scores[0])[::-1]

    # Exclude the given product from the similar products list
    sorted_indices = sorted_indices[1:]

    # Retrieve the top N similar products
    N = 6  # Change N to the desired number of similar products
    similar_product_ids = [product_ids[idx] for idx in sorted_indices[:N]]

    # Retrieve the actual product details using the similar product ids
    similar_products = [
        product for product in products if product['product_id'] in similar_product_ids
    ]
    #print(similar_product_ids,similar_products,cos_sim_scores,sorted_indices,sep='\n')
    return similar_products

def getCategoryDesc(category_id, categories):
    for category in categories:
        if category['category_id'] == category_id:
            return category['description']
    else:
        raise Exception("Category not found. Contact Admin.")
