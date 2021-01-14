import re
import string

import nltk
import numpy as np
import pandas as pd
from nltk.corpus import stopwords

from preprocessing.common import remove_quotes, reduce_multiplied_letters


class TextPreprocessor:

    def __init__(self):
        nltk.download('stopwords')
        nltk.download('words')

        self.STOPWORDS = stopwords.words('english')
        self.STOPWORDS.append("rt")

        self.WORDS = set(nltk.corpus.words.words())
        self.WORDS.update({"fuck", "fucking", "fucked", "idiots", "shit"})

    def clean_sentence(self, sentence, **kwargs):
        df = pd.DataFrame(columns=["tweet"])
        df = df.append({'tweet': sentence}, ignore_index=True)
        self.clean_data_frame(df, **kwargs)
        return df['tweet'].iloc[0]

    def clean_data_frame(self, df, **kwargs):
        VADER = kwargs.get('VADER')
        # remove any quotes surrounding the tweet (3 times because there can be multiple)
        df["tweet"] = df["tweet"].apply(lambda x: remove_quotes(x))
        df["tweet"] = df["tweet"].apply(lambda x: remove_quotes(x))
        df["tweet"] = df["tweet"].apply(lambda x: remove_quotes(x))
        # to lower
        df["tweet"] = df["tweet"].apply(lambda x: x.lower())
        # spaces or #blablabla with spaces (leftmost)
        df["tweet"] = [re.sub('(@[^\s]+)|(#[^\s]+)', '', tweet) for tweet in df["tweet"]]
        # urls (leftmost)
        df["tweet"] = [re.sub('((www\.[^\s]+)|(https?://[^\s]+))','',tweet) for tweet in df["tweet"]]
        # something starting from single quote or ampresand (leftmost)
        df["tweet"] = [re.sub('(\'[^\s]+)|(&[^\s]+)','',tweet) for tweet in df["tweet"]]
        # everything what is not: word, space / : % . , - (leftmost)
        df["tweet"] = [re.sub('[^\w\s/:%.,_-]','',tweet) for tweet in df["tweet"]]
        if not VADER:
            # removes all single characters !"#$%&'()*+, -./:;<=>?@[\]^_`{|}~
            df["tweet"] = df["tweet"].apply(lambda tweet: tweet.translate(str.maketrans('', '', string.punctuation)))
        # removes all single characters 0123456789❤♀️♥⚽️《
        df["tweet"] = df["tweet"].apply(lambda tweet: tweet.translate(str.maketrans('', '', "0123456789❤♀️♥⚽️《")))
        df["tweet"] = df["tweet"].apply(lambda tweet: reduce_multiplied_letters(tweet))
        if not VADER:
            # removes all stopwords (look at comments below)
            df["tweet"] = df["tweet"].str.split(' ').apply(lambda tweet: ' '.join(k for k in tweet if k not in self.STOPWORDS))
        # removes all 'things' that are not in nltk words library
        df["tweet"] = df["tweet"].str.split(' ').apply(lambda tweet: ' '.join(k for k in tweet if k in self.WORDS))
        # replaces ' +' with ' ' for example: AAA +BBB -> AAA BBB
        df["tweet"] = df["tweet"].str.replace(' +', ' ', case=False)
        # removes blank characters at the begining and at the end
        df["tweet"] = df["tweet"].str.strip()
        # removes AAA300, 34HSF...
        df["tweet"].replace('', np.nan, inplace=True)
        # removes all tweets that has no value
        df.dropna(subset=["tweet"], inplace=True)

# STOPWORDS
# {‘ourselves’, ‘hers’, ‘between’, ‘yourself’, ‘but’, ‘again’, ‘there’, ‘about’, ‘once’, ‘during’, ‘out’, ‘very’, ‘having’,
# ‘with’, ‘they’, ‘own’, ‘an’, ‘be’, ‘some’, ‘for’, ‘do’, ‘its’, ‘yours’, ‘such’, ‘into’, ‘of’, ‘most’, ‘itself’, ‘other’,
# ‘off’, ‘is’, ‘s’, ‘am’, ‘or’, ‘who’, ‘as’, ‘from’, ‘him’, ‘each’, ‘the’, ‘themselves’, ‘until’, ‘below’, ‘are’, ‘we’,
# ‘these’, ‘your’, ‘his’, ‘through’, ‘don’, ‘nor’, ‘me’, ‘were’, ‘her’, ‘more’, ‘himself’, ‘this’, ‘down’, ‘should’, ‘our’,
# ‘their’, ‘while’, ‘above’, ‘both’, ‘up’, ‘to’, ‘ours’, ‘had’, ‘she’, ‘all’, ‘no’, ‘when’, ‘at’, ‘any’, ‘before’, ‘them’,
# ‘same’, ‘and’, ‘been’, ‘have’, ‘in’, ‘will’, ‘on’, ‘does’, ‘yourselves’, ‘then’, ‘that’, ‘because’, ‘what’, ‘over’, ‘why’,
# ‘so’, ‘can’, ‘did’, ‘not’, ‘now’, ‘under’, ‘he’, ‘you’, ‘herself’, ‘has’, ‘just’, ‘where’, ‘too’, ‘only’, ‘myself’, ‘which’,
# ‘those’, ‘i’, ‘after’, ‘few’, ‘whom’, ‘t’, ‘being’, ‘if’, ‘theirs’, ‘my’, ‘against’, ‘a’, ‘by’, ‘doing’, ‘it’, ‘how’,
# ‘further’, ‘was’, ‘here’, ‘than’}

    def debug_clean_data_frame(self, df, **kwargs):
        VADER = kwargs.get('VADER')
        # remove any quotes surrounding the tweet (3 times because there can be multiple)
        df["tweet"] = df["tweet"].apply(lambda x: remove_quotes(x))
        df["tweet"] = df["tweet"].apply(lambda x: remove_quotes(x))
        df["tweet"] = df["tweet"].apply(lambda x: remove_quotes(x))
        print(0)
        print(df.head())
        # to lower
        df["tweet"] = df["tweet"].apply(lambda x: x.lower())
        print(1)
        print(df.head())
        # spaces or #blablabla with spaces (leftmost)
        df["tweet"] = [re.sub('(@[^\s]+)|(#[^\s]+)', '', tweet) for tweet in df["tweet"]]
        print(2)
        print(df.head())
        # urls (leftmost)
        df["tweet"] = [re.sub('((www\.[^\s]+)|(https?://[^\s]+))','',tweet) for tweet in df["tweet"]]
        print(3)
        print(df.head())
        # something starting from single quote or ampresand (leftmost)
        df["tweet"] = [re.sub('(\'[^\s]+)|(&[^\s]+)','',tweet) for tweet in df["tweet"]]
        print(4)
        print(df.head())
        # everything what is not: word, space / : % . , - (leftmost)
        df["tweet"] = [re.sub('[^\w\s/:%.,_-]','',tweet) for tweet in df["tweet"]]
        print(5)
        print(df.head())
        if not VADER:
            # removes all single characters !"#$%&'()*+, -./:;<=>?@[\]^_`{|}~
            df["tweet"] = df["tweet"].apply(lambda tweet: tweet.translate(str.maketrans('', '', string.punctuation)))
            print(6)
            print(df.head())
        # removes all single characters 0123456789❤♀️♥⚽️《
        df["tweet"] = df["tweet"].apply(lambda tweet: tweet.translate(str.maketrans('', '', "0123456789❤♀️♥⚽️《")))
        print(7)
        print(df.head())
        df["tweet"] = df["tweet"].apply(lambda tweet: reduce_multiplied_letters(tweet))
        print('7a')
        print(df.head())
        if not VADER:
            # removes all stopwords (look at comments below)
            df["tweet"] = df["tweet"].str.split(' ').apply(lambda tweet: ' '.join(k for k in tweet if k not in self.STOPWORDS))
            print(8)
            print(df.head())
        # removes all 'things' that are not in nltk words library
        df["tweet"] = df["tweet"].str.split(' ').apply(lambda tweet: ' '.join(k for k in tweet if k in self.WORDS))
        print(9)
        print(df.head())
        # replaces ' +' with ' ' for example: AAA +BBB -> AAA BBB
        df["tweet"] = df["tweet"].str.replace(' +', ' ', case=False)
        print(10)
        print(df.head())
        # removes blank characters at the begining and at the end
        df["tweet"] = df["tweet"].str.strip()
        print(11)
        print(df.head())
        # removes AAA300, 34HSF...
        df["tweet"].replace('', np.nan, inplace=True)
        print(12)
        print(df.head())
        # removes all tweets that has no value
        df.dropna(subset=["tweet"], inplace=True)
        print(13)
        print(df.head())




"""
df_ = pd.DataFrame(columns=['tweet', 'label'])
df_ = df_.append({'tweet': "No shit?", 'label': 'hateful'}, ignore_index=True)
TextPreprocessor().debug_clean_data_frame(df_)
"""