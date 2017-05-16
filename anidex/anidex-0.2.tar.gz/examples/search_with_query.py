from anidex import Anidex

anidex = Anidex.Anidex()
print(anidex.search(query='Berserk',
                    lang_id='ENGLISH',
                    category=['ANIME_SUB', 'ANIME_RAW']))
