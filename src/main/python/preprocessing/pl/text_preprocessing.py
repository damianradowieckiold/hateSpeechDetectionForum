import re
import string

import morfeusz2 as morf
import nltk
import numpy as np
import pandas as pd

from preprocessing.common import remove_quotes, reduce_multiplied_letters


class TextPreprocessor:

    def __init__(self):
        nltk.download('punkt')
        nltk.download('pl196x')
        nltk.download('wordnet')
        self.STOPWORDS = set(nltk.corpus.stopwords.words('polish'))
        from nltk.corpus.reader import pl196x
        pl196x_dir = nltk.data.find('corpora/pl196x')
        pl = pl196x.Pl196xCorpusReader(pl196x_dir, r'.*\.xml', textids='textids.txt', cat_file="cats.txt")
        words = list(pl.words(fileids=pl.fileids(), categories='cats.txt'))
        from nltk.corpus import wordnet as wn
        words.extend(wn.words())
        self.WORDS = set(words)
        self.WORDS.update({"zdrajca", "zdrajco", "zdrajcy", "zdrajcami", "zdrajcę", "po", "pis",
                           "petru", "sprzedawczyk", "lewicka", "kaczyński", "tusk", "tvn", "tvp",
                           "polsat", "folksdojcz", "frajer", "frajerem"})
        self.morfeusz = morf.Morfeusz()

    def clean_sentence(self, sentence, **kwargs):
        df = pd.DataFrame(columns=["tweet"])
        df = df.append({'tweet': sentence}, ignore_index=True)
        self.clean_data_frame(df, **kwargs)
        return df['tweet'].iloc[0]

    def clean_data_frame(self, df, **kwargs):
        VADER = kwargs.get('VADER')
        LEMMATIZATION = kwargs.get('lemmatize')
        # remove any quotes surrounding the tweet (3 times because there can be multiple)
        df["tweet"] = df["tweet"].apply(lambda x: remove_quotes(x))
        df["tweet"] = df["tweet"].apply(lambda x: remove_quotes(x))
        df["tweet"] = df["tweet"].apply(lambda x: remove_quotes(x))
        # to lower
        df["tweet"] = df["tweet"].apply(lambda x: x.lower())
        # spaces or #blablabla with spaces (leftmost)
        df["tweet"] = [re.sub('(@[^\s]+)|(#[^\s]+)', '', tweet) for tweet in df["tweet"]]
        # urls (leftmost)
        df["tweet"] = [re.sub('((www\.[^\s]+)|(https?://[^\s]+))', '', tweet) for tweet in df["tweet"]]
        # something starting from single quote or ampresand (leftmost)
        df["tweet"] = [re.sub('(\'[^\s]+)|(&[^\s]+)', '', tweet) for tweet in df["tweet"]]
        # everything what is not: word, space / : % . , - (leftmost)
        df["tweet"] = [re.sub('[^\w\s/:%.,_-]', '', tweet) for tweet in df["tweet"]]
        if not VADER:
            # removes all single characters !"#$%&'()*+, -./:;<=>?@[\]^_`{|}~
            df["tweet"] = df["tweet"].apply(lambda tweet: tweet.translate(str.maketrans('', '', string.punctuation)))
        # removes all single characters 0123456789❤♀️♥⚽️《
        df["tweet"] = df["tweet"].apply(lambda tweet: tweet.translate(str.maketrans('', '', "0123456789❤♀️♥⚽️《")))
        if LEMMATIZATION:
            df['tweet'] = df['tweet'].apply(lambda x: self.lemmatize_and_join(x))
        df["tweet"] = df["tweet"].apply(lambda tweet: reduce_multiplied_letters(tweet))
        if not VADER:
            # removes all stopwords (look at comments below)
            df["tweet"] = df["tweet"].str.split(' ').apply(
                lambda tweet: ' '.join(k for k in tweet if k not in self.STOPWORDS))
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

    def lemmatize_and_join(self, comment):
        return " ".join(self.lemmatize(comment))

    def lemmatize(self, comment):
        analysis = self.morfeusz.analyse(comment)
        lemmas = []
        for interpretation in analysis:
            #print(interpretation)
            lemmas.append(interpretation[2][1].split(':')[0])

        #TODO it is better to look at indices
        return self.remove_duplicates(lemmas)

    def remove_duplicates(self, strings):
        seen = set()
        result = []
        for item in strings:
            if item not in seen:
                seen.add(item)
                result.append(item)
        return result

    def debug_clean_sentence(self, sentence, **kwargs):
        df = pd.DataFrame(columns=["tweet"])
        df = df.append({'tweet': sentence}, ignore_index=True)
        self.debug_clean_data_frame(df, **kwargs)
        return df['tweet'].iloc[0]

    def debug_clean_data_frame(self, df, **kwargs):
        VADER = kwargs.get('VADER')
        LEMMATIZATION = kwargs.get('lemmatize')
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
        df["tweet"] = [re.sub('((www\.[^\s]+)|(https?://[^\s]+))', '', tweet) for tweet in df["tweet"]]
        print(3)
        print(df.head())
        # something starting from single quote or ampresand (leftmost)
        df["tweet"] = [re.sub('(\'[^\s]+)|(&[^\s]+)', '', tweet) for tweet in df["tweet"]]
        print(4)
        print(df.head())
        # everything what is not: word, space / : % . , - (leftmost)
        df["tweet"] = [re.sub('[^\w\s/:%.,_-]', '', tweet) for tweet in df["tweet"]]
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
        if LEMMATIZATION:
            df['tweet'] = df['tweet'].apply(lambda x: self.lemmatize_and_join(x))
        print('7a')
        print(df.head())
        df["tweet"] = df["tweet"].apply(lambda tweet: reduce_multiplied_letters(tweet))
        print('7b')
        print(df.head())
        if not VADER:
            # removes all stopwords (look at comments below)
            df["tweet"] = df["tweet"].str.split(' ').apply(
                lambda tweet: ' '.join(k for k in tweet if k not in self.STOPWORDS))
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
cleaned_sentence = TextPreprocessor().debug_clean_sentence("Ale to był dobry groove!!!", lemmatize=True)
print(cleaned_sentence)
"""


"""
Wszelkie prawa zastrzeżone.

Redystrybucja i używanie, czy to w formie kodu źródłowego, czy w formie kodu wykonawczego, są dozwolone pod warunkiem spełnienia poniższych warunków:

Redystrybucja kodu źródłowego musi zawierać powyższą notę copyrightową, niniejszą listę warunków oraz poniższe oświadczenie o wyłączeniu odpowiedzialności.
Redystrybucja kodu wykonawczego musi zawierać powyższą notę copyrightową, niniejszą listę warunków oraz poniższe oświadczenie o wyłączeniu odpowiedzialności w dokumentacji i/lub w innych materiałach dostarczanych wraz z kopią oprogramowania.
NINIEJSZE OPROGRAMOWANIE JEST DOSTARCZONE PRZEZ WŁAŚCICIELI PRAW AUTORSKICH „TAKIM, JAKIE JEST”. KAŻDA, DOROZUMIANA LUB
BEZPOŚREDNIO WYRAŻONA GWARANCJA, NIE WYŁĄCZAJĄC DOROZUMIANEJ GWARANCJI PRZYDATNOŚCI HANDLOWEJ I PRZYDATNOŚCI DO OKREŚLONEGO ZASTOSOWANIA,
JEST WYŁĄCZONA. W ŻADNYM WYPADKU WŁAŚCICIELE PRAW AUTORSKICH NIE MOGĄ BYĆ ODPOWIEDZIALNI ZA JAKIEKOLWIEK BEZPOŚREDNIE, POŚREDNIE,
INCYDENTALNE, SPECJALNE, UBOCZNE I WTÓRNE SZKODY (NIE WYŁĄCZAJĄC OBOWIĄZKU DOSTARCZENIA PRODUKTU ZASTĘPCZEGO LUB SERWISU, ODPOWIEDZIALNOŚCI
Z TYTUŁU UTRATY WALORÓW UŻYTKOWYCH, UTRATY DANYCH LUB KORZYŚCI, A TAKŻE PRZERW W PRACY PRZEDSIĘBIORSTWA) SPOWODOWANE W JAKIKOLWIEK SPOSÓB
I NA PODSTAWIE ISTNIEJĄCEJ W TEORII ODPOWIEDZIALNOŚCI KONTRAKTOWEJ, CAŁKOWITEJ LUB DELIKTOWEJ (WYNIKŁEJ ZARÓWNO Z NIEDBALSTWA JAK INNYCH
POSTACI WINY), POWSTAŁE W JAKIKOLWIEK SPOSÓB W WYNIKU UŻYWANIA LUB MAJĄCE ZWIĄZEK Z UŻYWANIEM OPROGRAMOWANIA, NAWET JEŚLI O MOŻLIWOŚCI
POWSTANIA TAKICH SZKÓD OSTRZEŻONO.
"""