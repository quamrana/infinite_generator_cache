from functools import cache
from itertools import count

class infinite_generator_cache:
    def __init__(self, gen):
        self.wrapped = self.cache_of_wrapped_generators(gen)

    @cache
    def cache_of_wrapped_generators(self, gen):
        return self._make_wrapped_generator(gen())  # gen is called exactly once just here

    @staticmethod
    def _make_wrapped_generator(gen):
        @cache
        def wrapped(_):
            return next(gen)

        return wrapped

    @staticmethod
    def _make_counting_generator(wrapped):
        def counting():
            for n in count(1):
                yield wrapped(n)

        g = counting()
        return g

    def __call__(self):
        return self._make_counting_generator(self.wrapped)
