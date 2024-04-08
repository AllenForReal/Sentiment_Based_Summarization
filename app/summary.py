import os
from dotenv import load_dotenv
from openai import OpenAI
import google.generativeai as genai
import networkx as nx
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import sentiment

nltk.download('punkt')
nltk.download('stopwords')

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

def build_similarity_matrix(sentences):
    vectorizer = TfidfVectorizer()
    sentence_vectors = vectorizer.fit_transform(sentences).toarray()
    
    similarity_matrix = cosine_similarity(sentence_vectors)
    
    return similarity_matrix
    
def generate_summary_custom(text, num_sentences=2):
    sentences = sent_tokenize(text)
    similarity_matrix = build_similarity_matrix(sentences)
    
    # Create a graph and score nodes (sentences) based on their similarity
    graph = nx.from_numpy_array(similarity_matrix)
    text_rank_scores = nx.pagerank(graph)
    
    # Compute sentiment scores
    # sia = SentimentIntensityAnalyzer()
    # sentiment_scores = {i: sia.polarity_scores(sentences[i])['compound'] for i in range(len(sentences))}
    sentiment_scores = {sentiment.analyze_sentiment(sentence)}
    # Combine TextRank and sentiment scores
    combined_scores = {i: text_rank_scores[i] + sentiment_scores[i] for i in range(len(sentences))}
    
    # Sort sentences by combined score and select top ones as the summary
    ranked_sentences = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
    summary = ' '.join([sentences[i] for i, _ in ranked_sentences[:num_sentences]])
    return summary

