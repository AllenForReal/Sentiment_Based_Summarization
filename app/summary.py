import os
from dotenv import load_dotenv
from openai import OpenAI
import google.generativeai as genai
import runpod
import requests

load_dotenv()

def generate_summary_gpt(reviews, product_details):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    reviews_text = "- ".join([review['description'] for review in reviews])

    full_text = "Below are the reviews of a product:\n" + reviews_text + "\nWhat are the pros, cons, and verdict for this product?"

    review_data = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a review analyst, skilled in summaryzing various reviews for many differn types of products. You specialize in pin pointing the product's strong suits and short comings from a given review."},
        {"role": "user", "content": full_text}
    ]
    )
    
    name = product_details['name']
    full_description = product_details['full_description']
    feature_bullets = product_details['feature_bullets']

    description_data = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a product analyst, skilled in summaryzing various different types of products just from their product descriptions."},
        {"role": "user", "content": f"{name} - {full_description} - {feature_bullets}"}
    ]
    )

    return review_data.choices[0].message.content, description_data.choices[0].message.content

def generate_summary_gemini(reviews, product_details):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')

    reviews_text = "- ".join([review['description'] for review in reviews])

    full_text = "Below are the reviews of a product:\n" + reviews_text + "\nWhat are the pros, cons, and verdict for this product?"

    review_data = model.generate_content(full_text)
    
    name = product_details['name']
    full_description = product_details['full_description']
    feature_bullets = product_details['feature_bullets']
    
    product_data = model.generate_content(f"{name} - {full_description} - {feature_bullets}")

    return review_data.text, product_data

def generate_summary_custom(reviews, product_details):
    description_endpoint = "https://api.runpod.ai/v2/l8p1v5w0gct9w8/runsync"
    review_endpoint = "https://api.runpod.ai/v2/ida95h4l4ffo58/runsync"
    
    headers = {
        "Content-Type": "application/json", 
        "Authorization": f"Bearer {os.getenv('CUSTOM_API_KEY')}"
    }

    reviews_text = "- ".join([review['description'] for review in reviews])

    full_text = "Below are the reviews of a product:\n" + reviews_text + "\nWhat are the pros, cons, and verdict for this product?"

    review_body = {
        "input": {"text": full_text}
    }
    
    try:
        review_response = requests.post(review_endpoint, json=review_body, headers=headers)
        review_response.raise_for_status()
        review_data = review_response.json()
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None, None
    
    name = product_details['name']
    full_description = product_details['full_description']
    feature_bullets = product_details['feature_bullets']

    description_body = {
        "input": {"text": f"{name} - {full_description} - {feature_bullets}"}
    }
    
    try:
        description_response = requests.post(description_endpoint, json=description_body, headers=headers)
        description_response.raise_for_status()
        description_data = description_response.json()
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None, None

    return review_data['output'], description_data['output']