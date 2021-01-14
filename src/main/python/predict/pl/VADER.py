# Based on examples from project https://github.com/cjhutto/vaderSentiment
# **Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.**

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from preprocessing.pl.text_preprocessing import TextPreprocessor
from translate.translator import Translator


class VADER:

    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()
        self.text_preprocessor = TextPreprocessor()

    def translate_and_predict(self, sentence):
        translation = Translator().pl_to_en(sentence)
        return self.predict(translation)

    def predict(self, sentence):
        try:
            cleaned_sentence = self.text_preprocessor.clean_sentence(sentence, VADER=True, lemmatize=True)
        except IndexError:
            print("Omitting the sentence (VADER): " + str(sentence))
            return False
        polarity_scores = self.analyzer.polarity_scores(cleaned_sentence)
        return polarity_scores['compound'] < -0.09164180845721778


"""
if len(sys.argv) > 1:
    sentence_ = sys.argv[1]
else:
    sentence_ = input("Wprowadz linie do oceny (VADER): ")

print(VADER().translate_and_predict(sentence_))

"""


