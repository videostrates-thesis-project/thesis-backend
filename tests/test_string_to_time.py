import unittest

from src.thesis_backend.utils.string_to_time import string_to_time


class TestStringToTime(unittest.TestCase):
    def test_time_with_milliseconds(self):
        assert string_to_time("0:00:32.36") == 32.36
        assert string_to_time("0:00:32.3") == 32.3

    def test_time_without_milliseconds(self):
        assert string_to_time("0:00:32") == 32.0
