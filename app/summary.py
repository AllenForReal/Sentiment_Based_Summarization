import os
from openai import OpenAI

def generate_summary(text):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a review analyst, skilled in summaryzing various reviews for many differn types of products. You specialize in pin pointing the product's strong suits and short comings from a given review."},
        {"role": "user", "content": f"Summarize this review: {text}."}
    ]
    )

    return completion.choices[0].message.content