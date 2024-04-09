import os
from dotenv import load_dotenv
import requests

load_dotenv()

def scrape_amazon_product(product_id):
    reviews = []
 
    for i in range(1, 6):
        star = 'all_stars'
        if i == 5:
            star = 'five_star'
        elif i == 4:
            star = 'four_star'
        elif i == 3:
            star = 'three_star'
        elif i == 2:
            star = 'two_star'
        elif i == 1:
            star = 'one_star'
   
        review_payload = {'api_key': os.getenv('SCRAPER_API_KEY'),
            'asin': product_id,
            'country': 'us',
            'tld': 'com',
            'filter_by_star': star}

        r = requests.get('https://api.scraperapi.com/structured/amazon/review', params=review_payload)
        
        review_json = r.json()

        for review in review_json.get('reviews'):
            reviews.append({
                'rating': review['stars'],
                'description': review['review']
            })
            
    product_payload = {'api_key': os.getenv('SCRAPER_API_KEY'),
           'asin': product_id,
           'country': 'us',
           'tld': 'com'}

    p = requests.get('https://api.scraperapi.com/structured/amazon/product', params=product_payload)
    
    product_json = p.json()

    product_details = {
        'name': product_json.get('name'),
        'full_description': product_json.get('full_description'),
        'average_rating': product_json.get('average_rating'),
        'feature_bullets': product_json.get('feature_bullets')
    }

    return reviews, product_details