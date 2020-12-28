import pandas as pd

from translate.translator import Translator

file = r"zlosliwe"
all = pd.read_csv(r"..\resources\temp\%s.csv" % file)


def clean(tweet):
    return tweet.replace('"', "").replace("'", "")


for index, row in all.iterrows():
    current = pd.DataFrame({'tweet': [row[0]]})
    current['tweet'] = current['tweet'].apply(clean)
    try:
        current['tweet'] = current['tweet'].apply(Translator().pl_to_en)
    except:
        all.to_csv(r"..\resources\temp\%s.csv" % file, index=False)
        print('Failed on index:' + str(index))
        exit(-1)
    current.to_csv(r"..\resources\temp\%s_en.csv" % file, mode='a', index=False, header=False)
    all.drop(index, inplace=True)

result = pd.read_csv(r"..\resources\temp\%s_en.csv" % file)
print(result.head(10))
