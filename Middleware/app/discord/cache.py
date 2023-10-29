cache = {}

def cache_save(key, value):
    cache[key] = value

def cache_get(key):
    return cache[key]