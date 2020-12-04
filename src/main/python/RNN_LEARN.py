# Based on https://github.com/ybalcanci/Hate-Speech-Detector

import numpy as np
import pandas as pd
from keras import utils
from keras.layers import Dense, Activation, Dropout
from keras.models import Sequential
from keras.preprocessing import text
from sklearn.preprocessing import LabelEncoder

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

train_size = int(len(df) * .7)
train_posts = df['tweet'][:train_size]
train_tags = df['label'][:train_size]

test_posts = df['tweet'][train_size:]
test_tags = df['label'][train_size:]

max_words = 1000
tokenize = text.Tokenizer(num_words=max_words, char_level=False)
tokenize.fit_on_texts(train_posts) # only fit on train

x_train = tokenize.texts_to_matrix(train_posts)
x_test = tokenize.texts_to_matrix(test_posts)

encoder = LabelEncoder()
encoder.fit(train_tags)
y_train = encoder.transform(train_tags)
y_test = encoder.transform(test_tags)

num_classes = np.max(y_train) + 1
y_train = utils.to_categorical(y_train, num_classes)
y_test = utils.to_categorical(y_test, num_classes)

# Build the model
model = Sequential()
model.add(Dense(512, input_shape=(max_words,)))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes))
model.add(Activation('softmax'))
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

batch_size = 512
epochs = 30

history = model.fit(x_train, y_train,
                    batch_size=batch_size,
                    epochs=epochs,
                    verbose=1,
                    validation_split=0.1)

model.save(r"model\rnn_model")