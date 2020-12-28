# Based on https://github.com/ybalcanci/Hate-Speech-Detector
import warnings

from keras import utils
from sklearn.preprocessing import LabelEncoder

warnings.simplefilter(action='ignore', category=FutureWarning)
import nltk
import re
import string
import numpy as np
import pickle

from nltk.corpus import stopwords
#stderr = sys.stderr
#sys.stderr = open(os.devnull, 'w')
from tensorflow import keras
from df.loader import load_polish_all


#load model
model = keras.models.load_model(r"..\..\model\en\rnn_model2")

STOPWORDS = stopwords.words('english')
STOPWORDS.append("rt")

WORDS = set(nltk.corpus.words.words())
WORDS.update({"fuck", "fucking"})

df = load_polish_all()

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

with open(r"..\..\model\en\rnn_tokenizer", 'rb') as handle:
    tokenize = pickle.load(handle)

x_test = tokenize.texts_to_matrix(test_posts)

train_size = int(len(df) * .0)

test_posts = df['tweet'][train_size:]
test_tags = df['label'][train_size:]


encoder = LabelEncoder()
encoder.fit(test_tags)
y_test = encoder.transform(test_tags)
num_classes = np.max(y_test) + 1
y_test = utils.to_categorical(y_test, num_classes)

from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report

y_pred = model.predict(x_test)

for i in range(len(y_test)):
    if(y_pred[i][0] > y_pred[i][1]):
        y_pred[i][0] = 1
        y_pred[i][1] = 0
    else:
        y_pred[i][0] = 0
        y_pred[i][1] = 1

print(encoder.inverse_transform([0]))
print(encoder.inverse_transform([1]))
print(y_pred[:10])
print(y_test[:10])
print('accuracy %s' % accuracy_score(y_pred, y_test))
print(classification_report(y_test, y_pred))
