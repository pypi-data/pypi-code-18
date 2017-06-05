from pprint import pprint

from vizontele.crawler import Crawler

episode = Crawler('dizibox', 'doctor-who', 10, 8).get_sources()
assert len(episode['video_links']) > 0
pprint('Dizibox test successful')

episode = Crawler('dizimek', 'game of thrones', 1, 1).get_sources()
assert len(episode['video_links']) > 0
pprint('Dizimek test successful')

episode = Crawler('dizist', 'family-guy', 1, 1).get_sources()
assert len(episode['video_links']) > 0
pprint('Dizist test successful')

episode = Crawler('dizimag', 'supernatural', 12, 22).get_sources()
assert len(episode['video_links']) > 0
pprint('Dizimag test successful')

episode = Crawler('diziay', 'family guy', 1, 1).get_sources()
assert len(episode['video_links']) > 0
pprint('Diziay test successful')

episode = Crawler('sezonlukdizi', 'legion', 1, 4).get_sources()
assert len(episode['video_links']) > 0
pprint('Sezonlukdizi test successful')

episode = Crawler('dizilab', 'brooklyn-nine-nine', 4, 19).get_sources()
assert len(episode['video_links']) > 0
pprint('Dizilab test successful')

episode = Crawler('dizipub', 'legion', 1, 2).get_sources()
assert len(episode['video_links']) > 0
pprint('Dizipub test successful')