# Infinite Generator Cache
A `decorator` which is a cache for an infinite generator. This is useful when the generator takes time to generate each value.

This cache is specifically for pure functions (generators), that is functions which will always produce the same sequence of values everytime. So this is not suitable for values that might vary over time.
