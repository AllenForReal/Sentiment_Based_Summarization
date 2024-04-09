from flask import Flask, request, jsonify
from flask_cors import CORS
from scrape import scrape_amazon_product
from sentiment import analyze_sentiment_nltk, analyze_sentiment_lstm, analyze_sentiment_textblob
from summary import generate_summary_gpt, generate_summary_gemini, generate_summary_custom
import random

app = Flask(__name__)

CORS(app)

def analyzeProduct(product_id, classifier, model):
    reviews, product_details = scrape_amazon_product(product_id)
    if reviews:
        average_sentiment = calculateSentiment(reviews, classifier)
        summary, description = calculateSummary(reviews, product_details, model)
        
        return average_sentiment, summary, description
    
    return None, None, None

def calculateSentiment(reviews, classifier):
    sentiment_scores = []
    for review in reviews:
        if classifier == 'nltk':
            sentiment_scores.append(analyze_sentiment_nltk(review['description']))
        elif classifier == 'textblob':
            sentiment_scores.append(analyze_sentiment_textblob(review['description']))
        elif classifier == 'lstm':
            sentiment_scores.append(analyze_sentiment_lstm(review['description']))

    average_sentiment = sum(sentiment_scores) / len(sentiment_scores)

    return average_sentiment

def calculateSummary(reviews, product_details, model):
    if len(reviews) < 10:
        selected_reviews = reviews
    else:
        selected_reviews = random.sample(reviews, 10)
    
    if model == 'gpt':
        return generate_summary_gpt(selected_reviews, product_details)
    elif model == 'gemini':
        return generate_summary_gemini(selected_reviews, product_details)
    elif model == 'custom':
        return generate_summary_custom(selected_reviews, product_details)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    product_id = data.get('productId')
    classifier = data.get('classifier')
    model = data.get('model')
    sentiment, summary, description = analyzeProduct(product_id, classifier, model)
    response = {
        'sentiment': sentiment,
        'summary': summary,
        'description': description
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)