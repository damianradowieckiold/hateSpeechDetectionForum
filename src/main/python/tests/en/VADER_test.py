# Based on examples from project https://github.com/cjhutto/vaderSentiment
# **Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.**

import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from df.loader import load_polish_all

df = load_polish_all()

result = pd.DataFrame(columns=["label"])

analyzer = SentimentIntensityAnalyzer()

for index, row in df.iterrows():
    polarity_scores = analyzer.polarity_scores(row['tweet'])
    result = result.append({'label': 'hateful' if (polarity_scores['compound'] < -0.09799749720143784) else 'normal'}, ignore_index=True)

from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report

print('accuracy %s' % accuracy_score(result['label'], df['label']))
print(classification_report(df['label'], result['label'],target_names=['hateful', 'normal']))



# accuracy 0.39726612558735586
# precision    recall  f1-score   support
#
# hateful       0.71      0.16      0.26      4685
# normal       0.34      0.87      0.49      2338
#
# accuracy                           0.40      7023
# macro avg       0.53      0.52      0.38      7023
# weighted avg       0.59      0.40      0.34      7023
