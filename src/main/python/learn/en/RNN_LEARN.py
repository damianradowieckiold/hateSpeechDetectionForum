# Based on https://github.com/ybalcanci/Hate-Speech-Detector

import pickle

import numpy as np
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras import utils
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing import text

from df.loader import load_tweets, load_english_train

# xlsx from https://github.com/ybalcanci/Hate-Speech-Detector
df = load_tweets()
df = df.append(load_english_train())


import nltk
nltk.download('stopwords')
nltk.download('words')
from preprocessing.en.TextPreprocessing import TextPreprocessor

TextPreprocessor().clean_data_frame(df)

train_posts = df['tweet']
train_tags = df['label']


max_words = 1000
# keras.preprocessing 
tokenize = text.Tokenizer(num_words=max_words, char_level=False)
tokenize.fit_on_texts(train_posts) # only fit on train

with open(r"..\..\model\en\rnn_tokenizer", 'wb') as handle:
    pickle.dump(tokenize, handle, protocol=pickle.HIGHEST_PROTOCOL)

x_train = tokenize.texts_to_matrix(train_posts)

encoder = LabelEncoder()
encoder.fit(train_tags)
y_train = encoder.transform(train_tags)

num_classes = np.max(y_train) + 1
y_train = utils.to_categorical(y_train, num_classes)

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

model.fit(x_train, y_train, batch_size=batch_size,
    epochs=epochs,
    verbose=1,
    validation_split=0.1)

model.save(r"..\..\model\en\rnn_model2")