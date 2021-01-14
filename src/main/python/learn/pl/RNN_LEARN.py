import pickle
from os import path

import numpy as np
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras import utils
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing import text

from df.loader import load_polish_train, load_forum_hate_speech

# xlsx from https://github.com/ybalcanci/Hate-Speech-Detector
df = load_polish_train()
df = df.append(load_forum_hate_speech(), ignore_index=True)

from preprocessing.pl.text_preprocessing import TextPreprocessor

TextPreprocessor().clean_data_frame(df, lemmatize=True)

train_posts = df['tweet']
train_tags = df['label']

max_words = 1000
# keras.preprocessing 
tokenize = text.Tokenizer(num_words=max_words, char_level=False)
tokenize.fit_on_texts(train_posts) # only fit on train

with open(r"..\..\model\pl\rnn_tokenizer", 'wb') as handle:
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

base_path = path.dirname(__file__)
path_ = path.abspath(path.join(base_path, "..", "..", "model", "pl", "rnn_model"))
model.save(path_)