import unittest
import time

from src.thesis_backend.utils.throttle import throttle


class TestClass:
    def __init__(self):
        self.__value = 0

    @throttle(interval=1)
    def value(self):
        self.__value += 1
        return self.__value


class TestClass2:
    def __init__(self):
        self.__values = {}

    @throttle(interval=1)
    def value(self, key: str = 'default'):
        self.__values[key] = self.__values.get(key, 0) + 1
        return self.__values[key]


class TestWithAutoRefreshDecorator(unittest.TestCase):
    def setUp(self) -> None:
        self.test_class1_1 = TestClass()
        self.test_class1_2 = TestClass()
        self.test_class2 = TestClass2()

    def test_cache_is_not_shared_between_classes(self):
        assert self.test_class1_1.value() == 1
        time.sleep(1)
        assert self.test_class1_1.value() == 2
        assert self.test_class2.value() == 1

    def test_refresh_time_is_not_shared_between_instances_of_the_same_class(self):
        assert self.test_class1_2.value() == 1
        time.sleep(1)
        assert self.test_class1_2.value() == 2
        assert self.test_class1_1.value() == 1

    def test_caching_for_different_args(self):
        assert self.test_class2.value() == 1
        time.sleep(1)
        assert self.test_class2.value() == 2
        assert self.test_class2.value("other") == 1
