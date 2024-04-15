import nltk
import nltk.sentiment
import BERT
import LSTM

def analyze_sentiment_nltk(text):
    words = nltk.word_tokenize(text)
    
    tagged_words = nltk.pos_tag(words)
    
    analyzer = nltk.sentiment.vader.SentimentIntensityAnalyzer()
    sentiment_scores = []
    for word, tag in tagged_words:
        sentiment_scores.append(analyzer.polarity_scores(word)['compound'])
    
    average_sentiment = sum(sentiment_scores) / len(sentiment_scores)
    
    return average_sentiment

def analyze_sentiment_bert(text):
    return BERT.predict_sentiment(text)

def analyze_sentiment_lstm(text):
    return LSTM.predict_sentiment(text)