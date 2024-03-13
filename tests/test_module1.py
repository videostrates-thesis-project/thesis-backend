from src.thesis_backend import Module1


def test_module1():
    x = Module1().x()
    assert x == 1
