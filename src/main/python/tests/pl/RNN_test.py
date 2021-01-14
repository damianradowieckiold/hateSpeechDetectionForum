# Based on https://github.com/ybalcanci/Hate-Speech-Detector
import warnings

from keras import utils
from sklearn.preprocessing import LabelEncoder

warnings.simplefilter(action='ignore', category=FutureWarning)
import numpy as np
import pickle

#stderr = sys.stderr
#sys.stderr = open(os.devnull, 'w')
from tensorflow import keras
from df.loader import load_polish_test
from preprocessing.pl.text_preprocessing import TextPreprocessor

#load model
model = keras.models.load_model(r"..\..\model\pl\rnn_model")


df = load_polish_test()

TextPreprocessor().clean_data_frame(df, lemmatize=True)

test_posts = df['tweet'][0:]

with open(r"..\..\model\pl\rnn_tokenizer", 'rb') as handle:
    tokenize = pickle.load(handle)

x_test = tokenize.texts_to_matrix(test_posts)

test_posts = df['tweet'][0:]
test_tags = df['label'][0:]


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
