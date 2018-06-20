from Parser import Parser
from iron_cache import *
from time import sleep
import json

# Create an client object
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
    v = json.dumps([ob.__dict__ for ob in op], indent=3)
    cache.put(cache="online_players", key=world, value=v)
    print('Cached online players for ' + str(world))


# main loop
while True:
    cache_online_players('legacy')
    cache_online_players('destiny')
    cache_online_players('spectrum')
    cache_online_players('pendulum')
    sleep(10)
