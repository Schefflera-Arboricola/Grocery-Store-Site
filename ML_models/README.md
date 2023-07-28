# Description

1. `similarProducts(given_product, products, categories,N=6)`

- returns a list of N products(dictionary of features) that are similar to the given_product
- similarity is based on the `product_description` i.e. `product_description = 2*product['name'] + ' ' + 2* getCategoryDesc(product['category_id'], categories) + ' ' + product['description']`  `category_description` is given more importance by multiplying it by 2
- [TF-IDF](https://goodboychan.github.io/python/datacamp/natural_language_processing/2020/07/17/04-TF-IDF-and-similarity-scores.html) technique is used to find the similarity between the product descriptions

<br>

2. `recommendProducts(products,categories,orderItems)`

- returns a list of products(dictionary of features) that are similar to the products in the orderItems(that has all the products in the last 5 orders)
- `similarProducts()` is used to get similar products for each product in the orderItems and then based on the frequency of the products in the similar products list, the products are recommended in order.

<br>

3. `people_also_bought(products,categories,orders,customers,N=6)`

- 