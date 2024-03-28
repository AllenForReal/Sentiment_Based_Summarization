from flask import Flask, request, jsonify
from flask_cors import CORS
from scrape import scrape_amazon_product
from sentiment import analyze_sentiment_nltk, analyze_sentiment_lstm, analyze_sentiment_textblob
from summary import generate_summary_gpt, generate_summary_gemini, generate_summary_custom

app = Flask(__name__)

CORS(app)

def analyzeProduct(product_id, classifier, model):
    reviews = scrape_amazon_product(product_id)
    if reviews:
        average_sentiment = calculateSentiment(reviews, classifier)
        summary = calculateSummary(reviews, model)

        return average_sentiment, summary
    
    return None, None

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

def calculateSummary(reviews, model):
    if model == 'gpt':
        return generate_summary_gpt(reviews[0]['description'])
    elif model == 'gemini':
        return generate_summary_gemini(reviews[0]['description'])
    elif model == 'custom':
        return generate_summary_custom(reviews[0]['description'])

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    product_id = data.get('productId')
    classifier = data.get('classifier')
    model = data.get('model')
    sentiment, summary = analyzeProduct(product_id, classifier, model)
    response = {
        'sentiment': sentiment,
        'summary': summary
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)