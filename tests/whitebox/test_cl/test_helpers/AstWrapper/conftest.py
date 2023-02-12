from textwrap import dedent

import pytest


@pytest.fixture
def source_example():
    return dedent("""
    def first_function():
        pass
    class FirstClass:
        def first_method(self):
            pass
    class SecondClass:
        def second_method(self):
            pass
    def second_function():
        pass
    if True:
        print('nothing but the truth')
    """)
