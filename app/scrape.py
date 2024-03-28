import requests
from bs4 import BeautifulSoup

def scrape_amazon_product(product_id):
    url = f"https://www.amazon.com/dp/{product_id}"
    
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    product_reviews = []
    for review in soup.select(".review"):
        rating = review.select_one(".review-rating").text.strip()
        description = review.select_one(".review-text").text.strip()
        product_reviews.append({
            "rating": rating,
            "description": description
        })

    return product_reviews