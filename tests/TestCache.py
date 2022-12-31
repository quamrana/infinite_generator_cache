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

    def test_when_called_the_generator_has_correct_name(self):
        self.whenFirstDecorationMade()
        self.thenFirstAsStringIncludesAll(['infinite_generator_cache object', 'containing <class',
                                           '_create_new_mock_generator_class.<locals>.MockGenerator'])
        self.whenFirstGeneratorIsCreated()
        self.thenFirstGeneratorAsStringIs('<generator object TestSingleGeneratorCached._create_new_mock_generator_class.<locals>.MockGenerator')

    def thenTwoDecoratorsAreNotEqual(self):
        self.shouldNotEqual(self.first, self.second)

    def thenWrappedGeneratorsAreEqual(self):
        self.shouldEqual(self.first.wrapped, self.second.wrapped)

    def whenFirstGeneratorIsCreated(self):
        self.first_generator = self.first()

    def thenFirstAsStringIncludesAll(self, expected):
        str_repr = str(self.first)
        result = all(item in str_repr for item in expected)
        self.shouldBeTrue(result, f'Every item in {expected} should be in {str_repr}')

    def thenFirstGeneratorAsStringIs(self, expected):
        str_repr = str(self.first_generator)
        result = str_repr.startswith(expected)
        self.shouldBeTrue(result, f'{expected} should be in {str_repr}')