import re
import string

import nltk
import numpy as np
from nltk.corpus import stopwords


class TextPreprocessor:

    def __init__(self):
        nltk.download('stopwords')
        nltk.download('words')

        self.STOPWORDS = stopwords.words('english')
        self.STOPWORDS.append("rt")

        self.WORDS = set(nltk.corpus.words.words())
        self.WORDS.update({"fuck", "fucking"})

    #TODO look at it, it sometimes removes all words... example: Hi, what's going on?
    def clean_data_frame(self, df):
        # to lower
        df["tweet"] = df["tweet"].apply(lambda x: x.lower())
        print(df.head())
        # spaces or #blablabla with spaces (leftmost)
        df["tweet"] = [re.sub('(@[^\s]+)|(#[^\s]+)', '', tweet) for tweet in df["tweet"]]
        print(df.head())
        # urls (leftmost)
        df["tweet"] = [re.sub('((www\.[^\s]+)|(https?://[^\s]+))','',tweet) for tweet in df["tweet"]]
        print(df.head())
        # something starting from single quote or ampresand (leftmost)
        df["tweet"] = [re.sub('(\'[^\s]+)|(&[^\s]+)','',tweet) for tweet in df["tweet"]]
        print(df.head())
        # everything what is not: word, space / : % . , - (leftmost)
        df["tweet"] = [re.sub('[^\w\s/:%.,_-]','',tweet) for tweet in df["tweet"]]
        print(df.head())
        # removes all single characters !"#$%&'()*+, -./:;<=>?@[\]^_`{|}~
        # TODO VADER don't like it
        df["tweet"] = df["tweet"].apply(lambda tweet: tweet.translate(str.maketrans('', '', string.punctuation)))
        print(df.head())
        # removes all single characters 0123456789❤♀️♥⚽️《
        df["tweet"] = df["tweet"].apply(lambda tweet: tweet.translate(str.maketrans('', '', "0123456789❤♀️♥⚽️《")))
        print(df.head())
        # removes all stopwords (look at comments below)
        # TODO VADER don't like it
        df["tweet"] = df["tweet"].str.split(' ').apply(lambda tweet: ' '.join(k for k in tweet if k not in self.STOPWORDS))
        print(df.head())
        # removes all 'things' that are not in nltk words library
        df["tweet"] = df["tweet"].str.split(' ').apply(lambda tweet: ' '.join(k for k in tweet if k in self.WORDS))
        print(df.head())
        # replaces ' +' with ' ' for example: AAA +BBB -> AAA BBB
        df["tweet"] = df["tweet"].str.replace(' +', ' ', case=False)
        print(df.head())
        # removes blank characters at the begining and at the end
        df["tweet"] = df["tweet"].str.strip()
        print(df.head())
        # removes AAA300, 34HSF...
        df["tweet"].replace('', np.nan, inplace=True)
        print(df.head())
        # removes all tweets that has no value
        df.dropna(subset=["tweet"], inplace=True)
        print(df.head())

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