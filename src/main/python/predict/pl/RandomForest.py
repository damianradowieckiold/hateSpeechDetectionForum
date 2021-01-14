import warnings

import joblib

warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
from translate.translator import Translator
from preprocessing.pl.text_preprocessing import TextPreprocessor
from os import path


class RandomForest:

    def __init__(self):
        base_path = path.dirname(__file__)
        file_path = path.abspath(path.join(base_path, "..", "..", "model", "pl", "rf_model"))
        self.rf = joblib.load(file_path)
        self.text_preprocessor = TextPreprocessor()

    def translate_and_predict(self, sentence):
        translation = Translator().pl_to_en(sentence)
        return self.predict(translation)

    def predict(self, sentence):
        data = {'tweet': [sentence], 'Age': 20}
        df = pd.DataFrame(data)
        self.text_preprocessor.clean_data_frame(df, lemmatize=True)
        try:
            return True if self.rf.predict([df['tweet'].iloc[0]]) == 'hateful' else False
        except IndexError:
            print("Omitting the sentence (Random Forest): " + str(sentence))
            return False

"""
if len(sys.argv) > 1:
    sentence_ = sys.argv[1]
else:
    sentence_ = input("Wprowadz linie do oceny (Random Forest): ")

print(RandomForest().translate_and_predict(sentence_))
"""