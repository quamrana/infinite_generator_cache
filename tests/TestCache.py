from qutest import TestCase
from infinite import infinite_generator_cache


# @infinite_generator_cache
class MockGenerator:
    number_of_calls = 0

    def __init__(self):
        MockGenerator.number_of_calls += 1


class TestSingleGeneratorCached(TestCase):
    def setUp(self):
        self.thenNumberOfCallsIs(0)

    def test_Mock_Generator_already_called(self):
        self.whenFirstDecorationMade()
        self.shouldEqual(MockGenerator.number_of_calls, 1)
        self.whenSecondDecorationMade()
        self.shouldEqual(MockGenerator.number_of_calls, 1)

    def thenNumberOfCallsIs(self, expected):
        self.shouldEqual(MockGenerator.number_of_calls, expected)

    def whenFirstDecorationMade(self):
        self.first = infinite_generator_cache(MockGenerator)

    def whenSecondDecorationMade(self):
        self.second = infinite_generator_cache(MockGenerator)
