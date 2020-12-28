import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# **Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.** 
# xlsx from https://github.com/ybalcanci/Hate-Speech-Detector
df = pd.read_excel(r"..\resources\external\hatespeech_text.xlsx", header = None)
df.rename(columns={0:'tweet', 1:'label'}, inplace=True)

import nltk
nltk.download('stopwords')
nltk.download('words')
from preprocessing.en.TextPreprocessing import TextPreprocessor

TextPreprocessor().clean_data_frame(df)

X = df.tweet
y = df.label

sum_neg_for_normal_tweets = 0.0
sum_neu_for_normal_tweets = 0.0
sum_pos_for_normal_tweets = 0.0
sum_compound_for_normal_tweets = 0.0

sum_neg_for_hatespeech_tweets = 0.0
sum_neu_for_hatespeech_tweets = 0.0
sum_pos_for_hatespeech_tweets = 0.0
sum_compound_for_hatespeech_tweets = 0.0

analyzer = SentimentIntensityAnalyzer()

#{'neg': 0.0, 'neu': 1.0, 'pos': 0.0, 'compound': 0.0}
for index, row in df.iterrows():
    polarity_scores = analyzer.polarity_scores(row['tweet'])
    if(row['label'] == 'hateful'):
        sum_neg_for_hatespeech_tweets += polarity_scores['neg']
        sum_neu_for_hatespeech_tweets += polarity_scores['neu']
        sum_pos_for_hatespeech_tweets += polarity_scores['pos']
        sum_compound_for_hatespeech_tweets += polarity_scores['compound']
    else:
        sum_neg_for_normal_tweets += polarity_scores['neg']
        sum_neu_for_normal_tweets += polarity_scores['neu']
        sum_pos_for_normal_tweets += polarity_scores['pos']
        sum_compound_for_normal_tweets += polarity_scores['compound']


avg_neg_for_normal_tweets = sum_neg_for_normal_tweets / len(df.index)
avg_neu_for_normal_tweets = sum_neu_for_normal_tweets / len(df.index)
avg_pos_for_normal_tweets = sum_pos_for_normal_tweets / len(df.index)
avg_compound_for_normal_tweets = sum_compound_for_normal_tweets / len(df.index)

avg_neg_for_hatespeech_tweets = sum_neg_for_hatespeech_tweets / len(df.index)
avg_neu_for_hatespeech_tweets = sum_neu_for_hatespeech_tweets / len(df.index)
avg_pos_for_hatespeech_tweets = sum_pos_for_hatespeech_tweets / len(df.index)
avg_compound_for_hatespeech_tweets = sum_compound_for_hatespeech_tweets / len(df.index)

print("---------------------")
print("---------------------")
print('--NORMAL TWEETS--')
print("Avg neg normal tweets", avg_neg_for_normal_tweets)
print("Avg neu normal tweets", avg_neu_for_normal_tweets)
print("Avg pos normal tweets", avg_pos_for_normal_tweets)
print("Avg compound normal tweets", avg_compound_for_normal_tweets)
print("---------------------")
print("--HATE SPEECH TWEETS--")
print("---------------------")
print("Avg neg hatespeech tweets", avg_neg_for_hatespeech_tweets)
print("Avg neu hatespeech tweets", avg_neu_for_hatespeech_tweets)
print("Avg pos hatespeech tweets", avg_pos_for_hatespeech_tweets)
print("Avg compound hatespeech tweets", avg_compound_for_hatespeech_tweets)
print("---------------------")
