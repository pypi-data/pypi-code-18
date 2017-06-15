from cypress_common.cypress_cache import CypressCache
import time

cache = CypressCache(host='10.0.80.111')

# a = time.time()
# p_ids = cache.get_profile_ids_by_category('ae019471-42de-4c05-a41f-0d5d0b98e8ab')
# print 'time spent: '
# print time.time() - a
# print len(p_ids)
# print p_ids[:10]
#

s = time.time()
imgs = []
pp_ids = cache.redis.hkeys("profile:vector")
for x in pp_ids:
    cat = x.split(':')[0]
    if cat == 'ae019471-42de-4c05-a41f-0d5d0b98e8ab1':
        img = x.split(':')[1]
        imgs.append(img)
print 'time spent: '
print time.time() - s
print len(imgs)
print imgs[:10]