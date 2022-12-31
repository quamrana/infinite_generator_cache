# Infinite Generator Cache
A `decorator` which is a cache for an infinite generator. This is useful when the generator takes time to generate each value.

This cache is specifically for pure functions (generators), that is functions which will always produce the same sequence of values everytime. So this is not suitable for values that might vary over time.

An infinite generator in python is like this:
```python
from itertools import count

def gen():
    for c in count(1):
        yield c
```
However, this is trivial. It's a wrapper around `count()`. As a programmer you would not bother to cache the results, you would just create a new generator every time it is needed.

What if the generator was less trivial in time? We can modify the above code to make it more expensive in time to generate each value:
```python
from itertools import count
from time import sleep

def gen():
    for c in count(1):
        sleep(0.1)
        yield c
```
Ok, so this is a degenerate case, and we have to imagine that it is some heavy computation or searching which really takes the time.

However, this decorator is easy to use:
```python
from itertools import count
from time import sleep
from infinite import infinite_generator_cache

@infinite_generator_cache
def gen():
    for c in count(1):
        sleep(0.1)
        yield c
```
You can still have multiple clients for this generator and a time cost has to be paid for each new number generated, but only the first one that retrieves a new number pays the time cost. All other clients which retrieve old numbers get it directly from the cache.

## Limitations

This decorator is limited to infinite generators.

This decorator is limited to generators which take no parameters.

This decorator provides no performance improvement if the generator is not reused.
