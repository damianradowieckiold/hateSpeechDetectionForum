import pandas as pd

df = pd.DataFrame(columns=["tweet", "label"])

grozby_karalne = pd.read_csv(r"..\resources\polish_comments\grozby_karalne.csv", names=["tweet"])
grozby_karalne['label'] = 'hateful'
df = df.append(grozby_karalne)

ostra_krytyka = pd.read_csv(r"..\resources\polish_comments\ostra_krytyka.csv", names=["tweet"])
ostra_krytyka['label'] = 'hateful'
df = df.append(ostra_krytyka)

obrazliwe = pd.read_csv(r"..\resources\polish_comments\obrazliwe.csv", names=["tweet"])
obrazliwe['label'] = 'hateful'
df = df.append(obrazliwe)

pozostale = pd.read_csv(r"..\resources\polish_comments\pozostale.csv", names=["tweet"])
pozostale['label'] = 'normal'
df = df.append(pozostale)

krytyka = pd.read_csv(r"..\resources\polish_comments\krytyka.csv", names=["tweet"])
krytyka['label'] = 'normal'
df = df.append(krytyka)

zlosliwe = pd.read_csv(r"..\resources\polish_comments\zlosliwe.csv", names=["tweet"])
zlosliwe['label'] = 'normal'
df = df.append(zlosliwe)

df.to_csv(r"..\resources\polish_comments\combined_polish.csv", index=False)








