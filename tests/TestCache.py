from qutest import TestCase
from infinite import infinite_generator_cache


# @infinite_generator_cache


class TestSingleGeneratorCached(TestCase):
    def setUp(self):
        self.MockGenerator = self._create_new_mock_generator_class()
        self.thenNumberOfCallsIs(0)

    @staticmethod
    def _create_new_mock_generator_class():
        class MockGenerator:
            number_of_calls = 0

            def __init__(self):
                MockGenerator.number_of_calls += 1

        return MockGenerator

    def test_Mock_Generator_already_called(self):
        self.whenFirstDecorationMade()
        self.thenNumberOfCallsIs(1)
        self.whenSecondDecorationMade()
        self.thenNumberOfCallsIs(1)

    def thenNumberOfCallsIs(self, expected):
        self.shouldEqual(self.MockGenerator.number_of_calls, expected)

    def whenFirstDecorationMade(self):
        self.first = infinite_generator_cache(self.MockGenerator)

    def whenSecondDecorationMade(self):
        self.second = infinite_generator_cache(self.MockGenerator)

    def test_Decorators_themselves_are_different_instances(self):
        self.whenFirstDecorationMade()
        self.whenSecondDecorationMade()
        self.thenTwoDecoratorsAreNotEqual()

    def test_Wrapped_Generators_are_same_instance(self):
        self.whenFirstDecorationMade()
        self.whenSecondDecorationMade()
        self.thenWrappedGeneratorsAreEqual()

    def thenTwoDecoratorsAreNotEqual(self):
        self.shouldNotEqual(self.first, self.second)

    def thenWrappedGeneratorsAreEqual(self):
        self.shouldEqual(self.first.wrapped, self.second.wrapped)
