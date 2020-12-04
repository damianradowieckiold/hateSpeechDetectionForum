# Based on https://github.com/ybalcanci/Hate-Speech-Detector

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

# xlsx from https://github.com/ybalcanci/Hate-Speech-Detector
df = pd.read_excel(r"..\resources\external\hatespeech_text.xlsx", header = None)
df.rename(columns={0:'tweet', 1:'label'}, inplace=True)

import nltk
nltk.download('stopwords')
nltk.download('words')
from nltk.corpus import stopwords
import re
import string

STOPWORDS = stopwords.words('english')
STOPWORDS.append("rt")

WORDS = set(nltk.corpus.words.words())
WORDS.update({"fuck", "fucking"})

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

# Data splitting
X = df.tweet
y = df.label
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state = 42)
from sklearn.feature_extraction.text import TfidfTransformer
cv = CountVectorizer()
tfidftrans = TfidfTransformer()
after_cv = cv.fit_transform(X_train)
after_tf = tfidftrans.fit_transform(after_cv)
from sklearn.linear_model import SGDClassifier

sgd = Pipeline([('vect', CountVectorizer()),
                ('tfidf', TfidfTransformer()),
                ('clf', SGDClassifier(loss='hinge', penalty='l2',alpha=1e-3, random_state=42, max_iter=5, tol=None)),
                ])
sgd.fit(X_train, y_train)

from sklearn.externals import joblib
joblib.dump(sgd, r"model\svm_model", compress = 1)