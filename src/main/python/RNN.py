# Based on https://github.com/ybalcanci/Hate-Speech-Detector
import nltk
nltk.download('stopwords')
nltk.download('words')
from nltk.corpus import stopwords
import re
import string

import numpy as np
import pandas as pd

from tensorflow import keras
from keras.preprocessing import text

#load model
model = keras.models.load_model(r"model\rnn_model")

STOPWORDS = stopwords.words('english')
STOPWORDS.append("rt")

WORDS = set(nltk.corpus.words.words())
WORDS.update({"fuck", "fucking"})


data = {'tweet':["You are a fucking slut",
                 "It is a beautiful day",
                 "Fuck you",
                 "There is nothing to do",
                 "Spotify is fucking with me https://t.co/lkYGXODb5P"
                 ], 'Age':[20,30,20,20,20]}

df = pd.DataFrame(data)

def clean_text():
    df["tweet"] = df["tweet"].apply(lambda x: x.lower())
    df["tweet"] = [re.sub('(@[^\s]+)|(#[^\s]+)', '', tweet) for tweet in df["tweet"]]
    df["tweet"] = [re.sub('((www\.[^\s]+)|(https?://[^\s]+))','',tweet) for tweet in df["tweet"]]
    df["tweet"] = [re.sub('(\'[^\s]+)|(&[^\s]+)','',tweet) for tweet in df["tweet"]]
    df["tweet"] = [re.sub('[^\w\s/:%.,_-]','',tweet) for tweet in df["tweet"]]
    df["tweet"] = df["tweet"].apply(lambda tweet: tweet.translate(str.maketrans('', '', string.punctuation)))
    df["tweet"] = df["tweet"].apply(lambda tweet: tweet.translate(str.maketrans('', '', "0123456789❤♀️♥⚽️《")) )
    df["tweet"] = df["tweet"].str.split(' ').apply(lambda tweet: ' '.join(k for k in tweet if k not in STOPWORDS))
    df["tweet"] = df["tweet"].str.split(' ').apply(lambda tweet: ' '.join(k for k in tweet if k in WORDS))
    df["tweet"] = df["tweet"].str.replace(' +', ' ', case=False)
    df["tweet"] = df["tweet"].str.strip()
    df["tweet"].replace('', np.nan, inplace=True)
    df.dropna(subset=["tweet"], inplace=True)

clean_text()

test_posts = df['tweet'][0:]

tokenize = text.Tokenizer(num_words=1000, char_level=False)

tokenize.fit_on_texts(test_posts)
x_test = tokenize.texts_to_matrix(test_posts)

y_pred = model.predict(x_test)

for i in range(5):
    if(y_pred[i][0] > y_pred[i][1]):
        y_pred[i][0] = 1
        y_pred[i][1] = 0
    else:
        y_pred[i][0] = 0
        y_pred[i][1] = 1
print(y_pred)