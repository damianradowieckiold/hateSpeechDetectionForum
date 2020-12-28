import warnings

import joblib

warnings.simplefilter(action='ignore', category=FutureWarning)
import sys
import pandas as pd
from translate.translator import Translator
from preprocessing.en.TextPreprocessing import TextPreprocessor
from os import path

def translate_and_predict(sentence):
    translation = Translator().pl_to_en(sentence)
    print(translation)
    return predict(translation)


def predict(sentence):
    data = {'tweet': [sentence], 'Age': 20}
    df = pd.DataFrame(data)
    TextPreprocessor().clean_data_frame(df)
    print(df.head())
    base_path = path.dirname(__file__)
    file_path = path.abspath(path.join(base_path, "..", "..", "model", "en", "rf_model"))
    rf = joblib.load(file_path)

    return True if rf.predict([df['tweet'].iloc[0]]) == 'hateful' else False


if len(sys.argv) > 1:
    sentence_ = sys.argv[1]
else:
    sentence_ = input("Wprowadz linie do oceny: ")

print(translate_and_predict(sentence_))
