#!/usr/bin/python3
'''exercise'''
import uuid
from functools import wraps
import redis
from typing import Union, Callable


class Cache:
    '''parent class'''

    def __init__(self):
        '''init method'''
        self._redis = redis.Redis()
        self._redis.flushdb()

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int]:
        '''
        get - to convert the data back to the desired format.
        args:
            key - string argument
            fn - optional callable argument
        return - string, bytes or int
        '''
        data = self._redis.get(key)
        if data is not None and fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        '''
        get_str - parametize to string version
        args:
            key - string variable
        return - string or none
        '''
        return self.get(key, fn=lambda d: d.decode("utf-8") if d else None)

    def get_int(self, key: str) -> Union[int, None]:
        '''
        get_int - parametize to string version
        args:
            key - string variable
        return - int or none
        '''
        return self.get(key, fn=lambda d: int(d) if d else None)

    def count_calls(method: Callable) -> Callable:
        '''
        count_calls - system counter
        args:
            method - callable
        return - callable
        '''
        counts = {}

        @wraps(method)
        def wrapper(self, *args, **kwargs):
            '''
            wrapper - callable function
            '''
            key = f"{method.__qualname__}"
            counts[key] = counts.get(key, 0) + 1
            self._redis.incr(key)
            return method(self, *args, **kwargs)

        return wrapper

    def call_history(method: Callable) -> Callable:
        '''
        call_history - store the history of inputs and outputs
        for a particular function
        args:
            method - callable parameter
        return - callable funcion
        '''
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            inputs_key = f"{method.__qualname__}:inputs"
            outputs_key = f"{method.__qualname__}:outputs"

            '''Store input parameters in Redis'''
            self._redis.rpush(inputs_key, str(args))

            '''Execute the wrapped function to retrieve the output'''
            output = method(self, *args, **kwargs)

            '''Store the output in Redis'''
            self._redis.rpush(outputs_key, str(output))

            return output

        return wrapper

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''
        store - store the input data in Redis using the random key
        args:
            data - string argument
        return - returns a string
        '''
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def replay(method):
        '''
        replay - display the history of calls of a particular function
        args:
            method -
        return - nothing
        '''
    inputs_key = f"{method.__qualname__}:inputs"
    outputs_key = f"{method.__qualname__}:outputs"

    inputs_history = cache._redis.lrange(inputs_key, 0, -1)
    outputs_history = cache._redis.lrange(outputs_key, 0, -1)

    print(f"{method.__qualname__} was called {len(inputs_history)} times:")

    for input_params, output_result in zip(inputs_history, outputs_history):
        input_params_str = input_params.decode("utf-8")
        output_result_str = output_result.decode("utf-8")
        print("{}(*{}) -> {}".format(
            method.__qualname__,
            {input_params_str},
            {output_result_str}))
