# Based on https://github.com/ybalcanci/Hate-Speech-Detector
import warnings


warnings.simplefilter(action='ignore', category=FutureWarning)
import sys
import pandas as pd
import pickle
from tensorflow import keras
from translate.translator import Translator
from preprocessing.en.TextPreprocessing import TextPreprocessor
from os import path


def translate_and_predict(sentence):
    translation = Translator().pl_to_en(sentence)
    return predict(translation)


def predict(sentence):
    base_path = path.dirname(__file__)
    file_path = path.abspath(path.join(base_path, "..", "..", "model", "en", "rnn_model2"))
    model = keras.models.load_model(file_path)

    data = {'tweet': [sentence], 'Age': 20}
    df = pd.DataFrame(data)

    TextPreprocessor().clean_data_frame(df)

    test_posts = df['tweet'][0:]

    base_path = path.dirname(__file__)
    file_path = path.abspath(path.join(base_path, "..", "..", "model", "en", "rnn_tokenizer"))

    with open(file_path, 'rb') as handle:
        tokenize = pickle.load(handle)

    x_test = tokenize.texts_to_matrix(test_posts)

    y_pred = model.predict(x_test)

    for i in range(len(data['tweet'])):
        if y_pred[i][0] > y_pred[i][1]:
            y_pred[i][0] = 1
            y_pred[i][1] = 0
        else:
            y_pred[i][0] = 0
            y_pred[i][1] = 1

    return True if y_pred[0][0] == 1.0 and (y_pred[0][1]) == 0.0 else False


if len(sys.argv) > 1:
    sentence_ = sys.argv[1]
else:
    sentence_ = input("Wprowadz linie do oceny: ")

print(translate_and_predict(sentence_))


