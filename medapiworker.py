from Parser import Parser
from iron_cache import *
import json

# Create an client object
cache = IronCache()
parser = Parser()

# Put an item
#for i in range(0, 5):
    #cache.put(cache="test_cache", key="mykey" + str(i), value="Cache" + str(i))

# Get an item
item = cache.get(cache="test_cache", key="mykey3")
print(item.value)

# Delete an item
# cache.delete(cache="test_cache", key="mykey")

# Increment an item in the cache
# cache.increment(cache="test_cache", key="mykey", amount=10)

# return json.dumps([ob.__dict__ for ob in online_players])

# main loop
#while True:
online_players = parser.get_online_players('legacy')
cache.put(cache="online_players", key="players", value=json.dumps([ob.__dict__ for ob in online_players]))
item = cache.get(cache="online_players", key="players")
print(item.value)
