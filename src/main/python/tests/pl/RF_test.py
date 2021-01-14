# Based on https://github.com/ybalcanci/Hate-Speech-Detector

import warnings

import joblib

warnings.simplefilter(action='ignore', category=FutureWarning)
from df.loader import load_polish_test
from sklearn.metrics import accuracy_score
from preprocessing.pl.text_preprocessing import TextPreprocessor

df = load_polish_test()

TextPreprocessor().clean_data_frame(df, lemmatize=True)

rf = joblib.load(r"..\..\model\pl\rf_model")

from sklearn.metrics import classification_report
y_pred = rf.predict(df['tweet'])

print('accuracy %s' % accuracy_score(y_pred, df['label']))
print(classification_report(df['label'], y_pred, target_names=['hateful', 'normal']))
