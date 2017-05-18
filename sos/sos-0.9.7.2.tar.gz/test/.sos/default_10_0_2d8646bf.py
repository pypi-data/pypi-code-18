import time
time.sleep(3)
with open("midfile.txt", 'w') as out:
    for i in range(1000):
        out.write('{}\n'.format(i))

