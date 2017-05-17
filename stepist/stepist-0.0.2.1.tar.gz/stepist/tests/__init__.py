import redis

data = []
def process_data(x):
    return 1
def save_result(x):
    return 1


r = redis.Redis()
for row in data:
    r.lpush('workers_queue', row)

while True:
    data = r.blpop('workers_queue')
    result = process_data(data)
    save_result(result)
