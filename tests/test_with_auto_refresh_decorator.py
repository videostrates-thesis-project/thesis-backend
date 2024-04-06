import unittest
import time

from src.thesis_backend.azure_video_indexer.azure_video_indexer import with_auto_refresh


class TestClass:
    def __init__(self):
        self.__value = 0

    def __refresh_value(self):
        self.__value += 1

    @property
    @with_auto_refresh(refresh_func=__refresh_value, refresh_interval=1)
    def value(self):
        return self.__value


class TestClass2:
    def __init__(self):
        self.__value = 0

    def __refresh_value(self):
        self.__value += 1

    @property
    @with_auto_refresh(refresh_func=__refresh_value, refresh_interval=1)
    def value(self):
        return self.__value


class TestWithAutoRefreshDecorator(unittest.TestCase):
    def setUp(self) -> None:
        self.test_class = TestClass()
        self.test_class2 = TestClass2()
        self.test_class3 = TestClass()

    def test_refresh_time_is_not_shared_between_classes(self):
        assert self.test_class.value == 1
        assert self.test_class.value == 1
        time.sleep(1)
        assert self.test_class.value == 2
        assert self.test_class.value == 2
        assert self.test_class2.value == 1
        assert self.test_class2.value == 1
        time.sleep(1)
        assert self.test_class.value == 3
        assert self.test_class.value == 3
        assert self.test_class2.value == 2
        assert self.test_class2.value == 2

    def test_refresh_time_is_not_shared_between_instances_of_the_same_class(self):
        assert self.test_class3.value == 1
        assert self.test_class3.value == 1
        time.sleep(1)
        assert self.test_class3.value == 2
        assert self.test_class3.value == 2
        assert self.test_class.value == 1
        assert self.test_class.value == 1
        assert self.test_class3.value == 2
        assert self.test_class3.value == 2
