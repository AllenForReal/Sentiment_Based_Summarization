import os
from dotenv import load_dotenv
from openai import OpenAI
import google.generativeai as genai

load_dotenv()

def generate_summary_gpt(text):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a review analyst, skilled in summaryzing various reviews for many differn types of products. You specialize in pin pointing the product's strong suits and short comings from a given review."},
        {"role": "user", "content": f"Summarize this review: {text}."}
    ]
    )

    return completion.choices[0].message.content

def generate_summary_gemini(text):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')

    response = model.generate_content(f"You are a review analyst, skilled in summaryzing various reviews for many differn types of products. You specialize in pin pointing the product's strong suits and short comings from a given review. Summarize this review: {text}.")
    
    return response.text

def generate_summary_custom(text):
    return "REVIEW FROM CUSTOM MODEL"