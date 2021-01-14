from os import path

import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline

from df.loader import load_polish_train, load_forum_hate_speech
from preprocessing.pl.text_preprocessing import TextPreprocessor

df = load_polish_train()
df = df.append(load_forum_hate_speech(), ignore_index=True)

TextPreprocessor().clean_data_frame(df, lemmatize=True)

X_train = df.tweet
y_train = df.label

rf = Pipeline([('vect', CountVectorizer()),
               ('tfidf', TfidfTransformer()),
               ('clf', RandomForestClassifier()),
               ])
rf.fit(X_train, y_train)

base_path = path.dirname(__file__)
path_ = path.abspath(path.join(base_path, "..", "..", "model", "pl", "rf_model"))
joblib.dump(rf, path_, compress=1)
