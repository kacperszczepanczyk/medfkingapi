from iron_cache import *

# Create an client object
cache = IronCache()

# Put an item
cache.put(cache="test_cache", key="mykey", value="Hello IronCache!")

# Get an item
item = cache.get(cache="test_cache", key="mykey")
print (item.value)

# Delete an item
cache.delete(cache="test_cache", key="mykey")

# Increment an item in the cache
cache.increment(cache="test_cache", key="mykey", amount=10)


