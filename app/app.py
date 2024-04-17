from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flasgger import Swagger
from flask_cors import CORS
from util import analyzeProduct
import nltk
import nltk.sentiment

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

CORS(app)

nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

class Analyze(Resource):
    def post(self):
        """
        This method responds to the POST request for this endpoint and returns the analysis of the Amazon Product.
        ---
        tags:
        - Product Analysis
        parameters:
            - name: productId
              in: query
              type: string
              required: true
              description: The ASIN to be analyzed
            - name: classifier
              in: query
              type: string
              required: true
              description: The classifier to be used for sentiment analysis
            - name: model
              in: query
              type: string
              required: true
              description: The model to be used for summary generation
        responses:
            200:
                description: A successful POST request
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                sentiment:
                                    type: string
                                    description: The sentiment of the product
                                summary:
                                    type: string
                                    description: The summary of the product
                                description:
                                    type: string
                                    description: The description of the product
        """
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
    
api.add_resource(Analyze, "/analyze")

if __name__ == '__main__':
    app.run(use_reloader=True)