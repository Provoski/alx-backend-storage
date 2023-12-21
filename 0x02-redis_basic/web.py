#!/usr/bin/env python3
'''web module'''
import requests
import redis
from functools import wraps
import time


# Redis setup
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

def cache_page(func):
    '''catch page'''
    @wraps(func)
    def wrapper(url):
        # Check if the result is already in the cache
        cache_key = f"cache:{url}"
        cached_result = redis_client.get(cache_key)

        if cached_result:
            print(f"Using cached result for {url}")
            return cached_result.decode("utf-8")

        # If not in the cache, call the original function
        result = func(url)

        # Store the result in the cache with expiration time of 10 seconds
        redis_client.setex(cache_key, 10, result)

        return result

    return wrapper

def count_access(func):
    '''count page access'''
    @wraps(func)
    def wrapper(url):
        # Increment the access count for the URL
        count_key = f"count:{url}"
        redis_client.incr(count_key)

        return func(url)

    return wrapper

@count_access
@cache_page
def get_page(url):
    '''get page'''
    response = requests.get(url)
    return response.text
