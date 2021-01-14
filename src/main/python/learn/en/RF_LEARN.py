# Based on https://github.com/ybalcanci/Hate-Speech-Detector

import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline

from df.loader import load_tweets, load_english_train
from preprocessing.en.TextPreprocessing import TextPreprocessor

# xlsx from https://github.com/ybalcanci/Hate-Speech-Detector
df = load_tweets()
df = df.append(load_english_train())

TextPreprocessor().clean_data_frame(df)

X_train = df.tweet
y_train = df.label
from sklearn.feature_extraction.text import TfidfTransformer
cv = CountVectorizer()
tfidftrans = TfidfTransformer()
after_cv = cv.fit_transform(X_train)
after_tf = tfidftrans.fit_transform(after_cv)
from sklearn.ensemble import RandomForestClassifier

rf = Pipeline([('vect', CountVectorizer()),
               ('tfidf', TfidfTransformer()),
               ('clf', RandomForestClassifier()),
               ])
rf.fit(X_train, y_train)

joblib.dump(rf, r"..\..\model\en\rf_model", compress=1)
