# Based on https://github.com/ybalcanci/Hate-Speech-Detector

import pickle

import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras import utils
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing import text


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


import nltk
nltk.download('stopwords')
nltk.download('words')
from preprocessing.en.TextPreprocessing import TextPreprocessor

TextPreprocessor().clean_data_frame(df)

train_size = int(len(df) * .7)
train_posts = df['tweet'][:train_size]
train_tags = df['label'][:train_size]

test_posts = df['tweet'][train_size:]
test_tags = df['label'][train_size:]

max_words = 1000
# keras.preprocessing 
tokenize = text.Tokenizer(num_words=max_words, char_level=False)
tokenize.fit_on_texts(train_posts) # only fit on train

tokenize.fit_on_texts(test_posts)
x_test = tokenize.texts_to_matrix(test_posts)

with open(r"model\rnn_tokenizer", 'wb') as handle:
    pickle.dump(tokenize, handle, protocol=pickle.HIGHEST_PROTOCOL)

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

model.fit(x_train, y_train, batch_size=batch_size,
    epochs=epochs,
    verbose=1,
    validation_split=0.1)

model.save(r"model\rnn_model2")