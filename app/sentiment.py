import nltk
import nltk.sentiment

def analyze_sentiment(text):
    words = nltk.word_tokenize(text)
    
    tagged_words = nltk.pos_tag(words)
    
    analyzer = nltk.sentiment.vader.SentimentIntensityAnalyzer()
    sentiment_scores = []
    for word, tag in tagged_words:
        sentiment_scores.append(analyzer.polarity_scores(word)['compound'])
    
    average_sentiment = sum(sentiment_scores) / len(sentiment_scores)
    
    return average_sentiment