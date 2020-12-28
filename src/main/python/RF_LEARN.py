# Based on https://github.com/ybalcanci/Hate-Speech-Detector

import joblib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from preprocessing.en.TextPreprocessing import TextPreprocessor


def hateful_comments(filename):
    comments = pd.read_csv(r"..\resources\polish_comments\%s.csv" % filename, names=["tweet"])
    comments['label'] = 'hateful'
    return comments

def normal_comments(filename):
    comments = pd.read_csv(r"..\resources\polish_comments\%s.csv" % filename, names=["tweet"])
    comments['label'] = 'normal'
    return comments

# xlsx from https://github.com/ybalcanci/Hate-Speech-Detector
df = pd.read_excel(r"..\resources\external\hatespeech_text.xlsx", header = None)
df.rename(columns={0:'tweet', 1:'label'}, inplace=True)

df.append(hateful_comments('grozby_karalne_en'))
df.append(hateful_comments('krytyka_en'))
df.append(hateful_comments('obrazliwe_en'))
df.append(hateful_comments('ostra_krytyka_en'))
df.append(hateful_comments('zlosliwe_en'))
df.append(normal_comments('pozostale_en'))


TextPreprocessor().clean_data_frame(df)

# Data splitting
X = df.tweet
y = df.label
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state = 42)
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


joblib.dump(rf, r"model\rf_model", compress = 1)