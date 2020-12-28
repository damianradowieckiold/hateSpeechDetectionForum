# Based on examples from project https://github.com/cjhutto/vaderSentiment
# **Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.**
import sys

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from translate.translator import Translator


def translate_and_predict(sentence):
    translation = Translator().pl_to_en(sentence)
    return predict(translation)


def predict(sentence):
    analyzer = SentimentIntensityAnalyzer()
    polarity_scores = analyzer.polarity_scores(sentence)
    return polarity_scores['compound'] < -0.09799749720143784


if len(sys.argv) > 1:
    sentence_ = sys.argv[1]
else:
    sentence_ = input("Wprowadz linie do oceny: ")

print(translate_and_predict(sentence_))


