from qutest import TestCase
from qutest import skip
from infinite import infinite_generator_cache


# @infinite_generator_cache

class CommonMethods:
    @staticmethod
    def _create_new_mock_generator_class():
        class MockGenerator:
            number_of_calls = 0
            number_of_next = 0

            def __init__(self):
                MockGenerator.number_of_calls += 1

            def __iter__(self):
                return self

            def __next__(self):
                MockGenerator.number_of_next += 1

        return MockGenerator
    def whenFirstDecorationMade(self):
        self.first = infinite_generator_cache(self.MockGenerator)
    def whenFirstGeneratorIsCreated(self):
        self.first_generator = self.first()
        self.first_generators = []


class TestSingleGeneratorCached(CommonMethods, TestCase):
    def setUp(self):
        self.MockGenerator = self._create_new_mock_generator_class()
        self.thenNumberOfCallsIs(0)


    def test_Mock_Generator_already_called(self):
        self.whenFirstDecorationMade()
        self.thenNumberOfCallsIs(1)
        self.whenSecondDecorationMade()
        self.thenNumberOfCallsIs(1)

    def thenNumberOfCallsIs(self, expected):
        self.shouldEqual(self.MockGenerator.number_of_calls, expected)


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
        self.thenFirstGeneratorAsStringIs('<generator object CommonMethods._create_new_mock_generator_class.<locals>.MockGenerator')

    def thenTwoDecoratorsAreNotEqual(self):
        self.shouldNotEqual(self.first, self.second)

    def thenWrappedGeneratorsAreEqual(self):
        self.shouldEqual(self.first.wrapped, self.second.wrapped)

    def thenFirstAsStringIncludesAll(self, expected):
        str_repr = str(self.first)
        result = all(item in str_repr for item in expected)
        self.shouldBeTrue(result, f'Every item in {expected} should be in {str_repr}')

    def thenFirstGeneratorAsStringIs(self, expected):
        str_repr = str(self.first_generator)
        result = str_repr.startswith(expected)
        self.shouldBeTrue(result, f'{expected} should be in {str_repr}')

class TestValuesNotCachedUntilSecondInstanceStarts(CommonMethods, TestCase):
    def setUp(self):
        self.MockGenerator = self._create_new_mock_generator_class()

    def test_first_few_calls_to_next_not_cached(self):
        self.whenFirstDecorationMade()
        self.whenFirstGeneratorIsCreated()
        self.whenFirstGeneratorGivesSamples(10)
        self.thenGeneratorShowsCall(10)
        self.whenFirstGeneratorIsCreatedAgain()
        self.whenFirstGeneratorsAreSampled(10)
        self.thenGeneratorShowsCall(10)

    def whenFirstGeneratorGivesSamples(self, limit):
        for _ in range(limit):
            next(self.first_generator)

    def thenGeneratorShowsCall(self, expected):
        self.shouldEqual(self.MockGenerator.number_of_next, expected)

    def whenFirstGeneratorIsCreatedAgain(self):
        self.first_generators.append(self.first())

    def whenFirstGeneratorsAreSampled(self, limit):
        for _ in range(limit):
            for g in self.first_generators:
                next(g)
