from functools import cache, wraps
from itertools import count


class infinite_generator_cache:
    def __init__(self, gen):
        self.gen = gen
        self.wrapped = self._cache_of_wrapped_generators(gen)

    @classmethod
    @cache
    def _cache_of_wrapped_generators(cls, gen):
        return cls._make_wrapped_generator(gen())  # gen is called exactly once just here

    @staticmethod
    def _make_wrapped_generator(gen):
        @cache
        def wrapped(_):
            return next(gen)

        return wrapped

    def _make_counting_generator(self, wrapped):
        @wraps(self.gen)
        def counting():
            for n in count(1):
                yield wrapped(n)

        g = counting()
        return g

    def __call__(self):
        return self._make_counting_generator(self.wrapped)

    def __repr__(self):
        rep = super().__repr__()
        return f'{rep} containing {self.gen}'
