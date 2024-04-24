import unittest
from thesis_backend.utils.time_str_to_seconds import time_str_to_seconds


class TestStringToTime(unittest.TestCase):
    def test_time_with_milliseconds(self):
        assert time_str_to_seconds("0:00:32.36") == 32.36
        assert time_str_to_seconds("0:00:32.3") == 32.3

    def test_time_without_milliseconds(self):
        assert time_str_to_seconds("0:00:32") == 32.0
