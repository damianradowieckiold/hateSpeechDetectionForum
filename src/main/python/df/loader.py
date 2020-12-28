from os import path

import pandas as pd


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


def build_absolute_path_to_file(filename):
    base_path = path.dirname(__file__)
    return path.abspath(path.join(base_path, "..", "..", "resources", "polish_comments", filename))
