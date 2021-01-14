# Based on https://github.com/ybalcanci/Hate-Speech-Detector
import warnings


warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
import pickle
from tensorflow import keras
from translate.translator import Translator
from preprocessing.pl.text_preprocessing import TextPreprocessor
from os import path


class RNN:

    def __init__(self):
        base_path = path.dirname(__file__)
        file_path = path.abspath(path.join(base_path, "..", "..", "model", "pl", "rnn_model"))
        self.model = keras.models.load_model(file_path)
        base_path = path.dirname(__file__)
        file_path = path.abspath(path.join(base_path, "..", "..", "model", "pl", "rnn_tokenizer"))
        with open(file_path, 'rb') as handle:
            self.tokenize = pickle.load(handle)
        self.text_preprocessor = TextPreprocessor()

    def translate_and_predict(self, sentence):
        translation = Translator().pl_to_en(sentence)
        return self.predict(translation)

    def predict(self, sentence):
        data = {'tweet': [sentence], 'Age': 20}
        df = pd.DataFrame(data)

        self.text_preprocessor.clean_data_frame(df, lemmatize=True)

        test_posts = df['tweet'][0:]

        x_test = self.tokenize.texts_to_matrix(test_posts)

        try:
            y_pred = self.model.predict(x_test)
        except UnboundLocalError:
            print("Omitting the sentence (RNN): " + str(sentence))
            return False

        for i in range(len(data['tweet'])):
            if y_pred[i][0] > y_pred[i][1]:
                y_pred[i][0] = 1
                y_pred[i][1] = 0
            else:
                y_pred[i][0] = 0
                y_pred[i][1] = 1

        return True if y_pred[0][0] == 1.0 and (y_pred[0][1]) == 0.0 else False

"""
if len(sys.argv) > 1:
    sentence_ = sys.argv[1]
else:
    sentence_ = input("Wprowadz linie do oceny (RNN): ")

print(RNN().translate_and_predict(sentence_))
"""


