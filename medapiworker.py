from Parser import Parser
from iron_cache import *
import json
import asyncio
from multiprocessing import Process
import time
from threading import Thread


cache = IronCache()
parser = Parser()



# Put an item
#for i in range(0, 5):
    #cache.put(cache="test_cache", key="mykey" + str(i), value="Cache" + str(i))

# Get an item
#item = cache.get(cache="test_cache", key="mykey3")
#print(item.value)

# Delete an item
# cache.delete(cache="test_cache", key="mykey")

# Increment an item in the cache
# cache.increment(cache="test_cache", key="mykey", amount=10)

# return json.dumps([ob.__dict__ for ob in online_players])

def cache_online_players(world):
    op = parser.get_online_players(str(world))
    v = json.dumps([ob.as_dict() for ob in op])
    cache.put(cache="online_players", key=world, value=v)
    print('Cached online players for ' + str(world))


def cache_highscores(world, profession):
    hs = parser.get_highscores(world, profession)
    v = json.dumps(hs)
    cache.put(cache="highscores", key=world + '_' + profession, value=v)
    print('Cached higscores for  ' + str(world) + '_' + profession)


async def fetch_online_players(interval):
    while True:
        await asyncio.sleep(interval)
        cache_online_players('legacy')
        cache_online_players('destiny')
        cache_online_players('spectrum')
        cache_online_players('pendulum')


async def fetch_highscores(interval):
    while True:
        await asyncio.sleep(interval)
        cache_highscores('legacy', 'warriors')


def fetch_online_players1(interval):
    while True:
        time.sleep(interval)
        cache_online_players('legacy')
        cache_online_players('destiny')
        cache_online_players('spectrum')
        cache_online_players('pendulum')


def fetch_highscores1(interval):
    while True:
        time.sleep(interval)
        cache_highscores('legacy', 'warriors')


'''
async def run():
    await fetch_online_players(10)
    await fetch_highscores(10)
    '''

if __name__ == '__main__':
    p = Process(target=fetch_online_players1, args=(10,))
    p.start()
    #p.join()
    p1 = Process(target=fetch_highscores1, args=(10,))
    p1.start()
   # p1.join()

'''
loop = asyncio.get_event_loop()
asyncio.ensure_future(fetch_online_players(10))
asyncio.ensure_future(fetch_highscores(1*60))
loop.run_forever()
'''