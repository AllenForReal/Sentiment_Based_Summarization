from flask import Flask, request, jsonify
from flask_cors import CORS
from scrape import scrape_amazon_product
from sentiment import analyze_sentiment
from summary import generate_summary

app = Flask(__name__)

CORS(app)

def analyzeProduct(product_id):
    reviews = scrape_amazon_product(product_id)
    if reviews:
        average_sentiment = calculateSentiment(reviews)
        summary = calculateSummary(reviews)

        return average_sentiment, summary
    
    return None, None

def calculateSentiment(reviews):
    sentiment_scores = []
    for review in reviews:
        sentiment_scores.append(analyze_sentiment(review['description']))
    average_sentiment = sum(sentiment_scores) / len(sentiment_scores)

    return average_sentiment

def calculateSummary(reviews):
    return generate_summary(reviews[0]['description'])

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    product_id = data.get('productId')
    sentiment, summary = analyzeProduct(product_id)
    response = {
        'sentiment': sentiment,
        'summary': summary
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)