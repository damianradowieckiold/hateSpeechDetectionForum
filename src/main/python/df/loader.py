from os import path

import pandas as pd


def load_polish_train():
    df = pd.DataFrame(columns=["tweet", "label"])

    grozby_karalne = pd.read_csv(build_absolute_path_to_file("grozby_karalne.csv"), names=["tweet"])
    grozby_karalne['label'] = 'hateful'
    df = df.append(grozby_karalne.head(31))

    ostra_krytyka = pd.read_csv(build_absolute_path_to_file("ostra_krytyka.csv"), names=["tweet"])
    ostra_krytyka['label'] = 'hateful'
    df = df.append(ostra_krytyka.head(621))

    obrazliwe = pd.read_csv(build_absolute_path_to_file("obrazliwe.csv"), names=["tweet"])
    obrazliwe['label'] = 'hateful'
    df = df.append(obrazliwe.head(1450))

    pozostale = pd.read_csv(build_absolute_path_to_file("pozostale.csv"), names=["tweet"])
    pozostale['label'] = 'normal'
    df = df.append(pozostale.head(1819))

    krytyka = pd.read_csv(build_absolute_path_to_file("krytyka.csv"), names=["tweet"])
    krytyka['label'] = 'hateful'
    df = df.append(krytyka.head(468))

    zlosliwe = pd.read_csv(build_absolute_path_to_file("zlosliwe.csv"), names=["tweet"])
    zlosliwe['label'] = 'hateful'
    df = df.append(zlosliwe.head(1071))

    return df


def load_polish_test():
    df = pd.DataFrame(columns=["tweet", "label"])

    grozby_karalne = pd.read_csv(build_absolute_path_to_file("grozby_karalne.csv"), names=["tweet"])
    grozby_karalne['label'] = 'hateful'
    df = df.append(grozby_karalne.tail(13))

    ostra_krytyka = pd.read_csv(build_absolute_path_to_file("ostra_krytyka.csv"), names=["tweet"])
    ostra_krytyka['label'] = 'hateful'
    df = df.append(ostra_krytyka.tail(266))

    obrazliwe = pd.read_csv(build_absolute_path_to_file("obrazliwe.csv"), names=["tweet"])
    obrazliwe['label'] = 'hateful'
    df = df.append(obrazliwe.tail(621))

    pozostale = pd.read_csv(build_absolute_path_to_file("pozostale.csv"), names=["tweet"])
    pozostale['label'] = 'normal'
    df = df.append(pozostale.tail(779))

    krytyka = pd.read_csv(build_absolute_path_to_file("krytyka.csv"), names=["tweet"])
    krytyka['label'] = 'hateful'
    df = df.append(krytyka.tail(200))

    zlosliwe = pd.read_csv(build_absolute_path_to_file("zlosliwe.csv"), names=["tweet"])
    zlosliwe['label'] = 'hateful'
    df = df.append(zlosliwe.tail(459))

    return df


def load_english_train():
    df = pd.DataFrame(columns=["tweet", "label"])

    grozby_karalne = pd.read_csv(build_absolute_path_to_file("grozby_karalne_en.csv"), names=["tweet"])
    grozby_karalne['label'] = 'hateful'
    df = df.append(grozby_karalne.head(31))

    ostra_krytyka = pd.read_csv(build_absolute_path_to_file("ostra_krytyka_en.csv"), names=["tweet"])
    ostra_krytyka['label'] = 'hateful'
    df = df.append(ostra_krytyka.head(621))

    obrazliwe = pd.read_csv(build_absolute_path_to_file("obrazliwe_en.csv"), names=["tweet"])
    obrazliwe['label'] = 'hateful'
    df = df.append(obrazliwe.head(1450))

    pozostale = pd.read_csv(build_absolute_path_to_file("pozostale_en.csv"), names=["tweet"])
    pozostale['label'] = 'normal'
    df = df.append(pozostale.head(1819))

    krytyka = pd.read_csv(build_absolute_path_to_file("krytyka_en.csv"), names=["tweet"])
    krytyka['label'] = 'hateful'
    df = df.append(krytyka.head(468))

    zlosliwe = pd.read_csv(build_absolute_path_to_file("zlosliwe_en.csv"), names=["tweet"])
    zlosliwe['label'] = 'hateful'
    df = df.append(zlosliwe.head(1071))

    return df


def load_english_test():

    df = pd.DataFrame(columns=["tweet", "label"])

    grozby_karalne = pd.read_csv(build_absolute_path_to_file("grozby_karalne_en.csv"), names=["tweet"])
    grozby_karalne['label'] = 'hateful'
    df = df.append(grozby_karalne.tail(13))

    ostra_krytyka = pd.read_csv(build_absolute_path_to_file("ostra_krytyka_en.csv"), names=["tweet"])
    ostra_krytyka['label'] = 'hateful'
    df = df.append(ostra_krytyka.tail(266))

    obrazliwe = pd.read_csv(build_absolute_path_to_file("obrazliwe_en.csv"), names=["tweet"])
    obrazliwe['label'] = 'hateful'
    df = df.append(obrazliwe.tail(621))

    pozostale = pd.read_csv(build_absolute_path_to_file("pozostale_en.csv"), names=["tweet"])
    pozostale['label'] = 'normal'
    df = df.append(pozostale.tail(779))

    krytyka = pd.read_csv(build_absolute_path_to_file("krytyka_en.csv"), names=["tweet"])
    krytyka['label'] = 'hateful'
    df = df.append(krytyka.tail(200))

    zlosliwe = pd.read_csv(build_absolute_path_to_file("zlosliwe_en.csv"), names=["tweet"])
    zlosliwe['label'] = 'hateful'
    df = df.append(zlosliwe.tail(459))

    return df


def load_polish_all():
    df = pd.DataFrame(columns=["tweet", "label"])

    grozby_karalne = pd.read_csv(build_absolute_path_to_file("grozby_karalne.csv"), names=["tweet"])
    grozby_karalne['label'] = 'hateful'
    df = df.append(grozby_karalne)

    ostra_krytyka = pd.read_csv(build_absolute_path_to_file("ostra_krytyka.csv"), names=["tweet"])
    ostra_krytyka['label'] = 'hateful'
    df = df.append(ostra_krytyka)

    obrazliwe = pd.read_csv(build_absolute_path_to_file("obrazliwe.csv"), names=["tweet"])
    obrazliwe['label'] = 'hateful'
    df = df.append(obrazliwe)

    pozostale = pd.read_csv(build_absolute_path_to_file("pozostale.csv"), names=["tweet"])
    pozostale['label'] = 'normal'
    df = df.append(pozostale)

    krytyka = pd.read_csv(build_absolute_path_to_file("krytyka.csv"), names=["tweet"])
    krytyka['label'] = 'hateful'
    df = df.append(krytyka)

    zlosliwe = pd.read_csv(build_absolute_path_to_file("zlosliwe.csv"), names=["tweet"])
    zlosliwe['label'] = 'hateful'
    df = df.append(zlosliwe)

    return df


def load_english_all():
    df = pd.DataFrame(columns=["tweet", "label"])

    grozby_karalne = pd.read_csv(build_absolute_path_to_file("grozby_karalne_en.csv"), names=["tweet"])
    grozby_karalne['label'] = 'hateful'
    df = df.append(grozby_karalne)

    ostra_krytyka = pd.read_csv(build_absolute_path_to_file("ostra_krytyka_en.csv"), names=["tweet"])
    ostra_krytyka['label'] = 'hateful'
    df = df.append(ostra_krytyka)

    obrazliwe = pd.read_csv(build_absolute_path_to_file("obrazliwe_en.csv"), names=["tweet"])
    obrazliwe['label'] = 'hateful'
    df = df.append(obrazliwe)

    pozostale = pd.read_csv(build_absolute_path_to_file("pozostale_en.csv"), names=["tweet"])
    pozostale['label'] = 'normal'
    df = df.append(pozostale)

    krytyka = pd.read_csv(build_absolute_path_to_file("krytyka_en.csv"), names=["tweet"])
    krytyka['label'] = 'hateful'
    df = df.append(krytyka)

    zlosliwe = pd.read_csv(build_absolute_path_to_file("zlosliwe_en.csv"), names=["tweet"])
    zlosliwe['label'] = 'hateful'
    df = df.append(zlosliwe)

    return df


def load_tweets():
    base_path = path.dirname(__file__)
    path_ = path.abspath(path.join(base_path, "..", "..", "resources", "external", "hatespeech_text.xlsx"))
    df = pd.read_excel(path_, header=None)
    df.rename(columns={0: 'tweet', 1: 'label'}, inplace=True)
    return df


def load_forum_hate_speech():
    base_path = path.dirname(__file__)
    path_ = path.abspath(path.join(base_path, "..", "..", "resources", "forum_comments", "hate_speech.csv"))
    df = pd.read_csv(path_, names=["tweet", "label"])
    return df


def build_absolute_path_to_file(filename):
    base_path = path.dirname(__file__)
    return path.abspath(path.join(base_path, "..", "..", "resources", "polish_comments", filename))
