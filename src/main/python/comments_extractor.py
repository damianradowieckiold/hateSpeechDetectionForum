# place this file in project https://github.com/krzjoa/Komentarze before run
from komentarze import Komentarze

komentarze = Komentarze()
komentarze.load()
df = komentarze.get_dataframe()
grozby_karalne = df[df.klasa == 'Groźby karalne']['komentarz']
grozby_karalne.to_csv(r'grozby_karalne.csv', index = False)
krytyka = df[df.klasa == 'Krytyka']['komentarz']
krytyka.to_csv(r'krytyka.csv', index = False)
obrazliwe = df[df.klasa == 'Obraźliwe']['komentarz']
obrazliwe.to_csv(r'obrazliwe.csv', index = False)
ostra_krytyka = df[df.klasa == 'Ostra krytyka']['komentarz']
ostra_krytyka.to_csv(r'ostra_krytyka.csv', index = False)
zlosliwe = df[df.klasa == 'Złośliwe']['komentarz']
zlosliwe.to_csv(r'zlosliwe.csv', index = False)
pozostale = df[df.klasa == 'Pozostałe']['komentarz']
pozostale.to_csv(r'pozostale.csv', index = False)
