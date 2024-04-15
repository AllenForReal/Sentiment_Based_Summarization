import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences # type: ignore
from tensorflow.keras.preprocessing.text import Tokenizer # type: ignore
import pickle
import numpy as np
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

def interpret_sentiment(probabilities):
    classes = ['Neutral', 'Negative', 'Positive']
    max_index = np.argmax(probabilities)

    return classes[max_index], probabilities[max_index]

model = tf.keras.models.load_model('app\model3.keras')

with open(r'app\tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    text = text.lower()

    text = re.sub(r'[^a-zA-Z0-9\s!?]', '', text)

    words = text.split()

    lemmatized = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]

    return ' '.join(lemmatized)

def predict_sentiment(text):
    preprocessed_text = preprocess_text(text)

    sequences = tokenizer.texts_to_sequences([preprocessed_text])
    
    padded_sequences = pad_sequences(sequences, maxlen=100)
    
    probabilities = model.predict(padded_sequences)
    
    sentiment, confidence = interpret_sentiment(probabilities[0])
    if sentiment == 'Neutral':
        return 0
    elif sentiment == 'Negative':
        return -confidence
    else:
        return confidence