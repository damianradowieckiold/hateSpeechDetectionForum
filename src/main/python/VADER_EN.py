# Based on examples from project https://github.com/cjhutto/vaderSentiment
# **Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.**

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def predict(sentence):
    analyzer = SentimentIntensityAnalyzer()
    polarity_scores = analyzer.polarity_scores(sentence)
    return polarity_scores['compound'] < -0.09799749720143784
