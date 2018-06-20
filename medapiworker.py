from iron_cache import *

# Create an client object
cache = IronCache()

# Put an item
for i in range(0, 5):
    cache.put(cache="test_cache", key="mykey" + str(i), value="Cache" + str(i))

# Get an item
item = cache.get(cache="test_cache", key="mykey3")
print (item.value)

# Delete an item
#cache.delete(cache="test_cache", key="mykey")

# Increment an item in the cache
#cache.increment(cache="test_cache", key="mykey", amount=10)


