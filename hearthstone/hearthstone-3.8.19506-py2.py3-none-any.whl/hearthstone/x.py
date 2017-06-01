from hearthstone import enums, stringsfile


for locale, member in enums.Locale.__members__.items():
	try:
		G = stringsfile.load_globalstrings(locale)
	except Exception as e:
		print(e)
		continue
	for k, cs in enums.CardSet.__members__.items():
		print([locale, k, G.get(cs.short_name_global, "")])
