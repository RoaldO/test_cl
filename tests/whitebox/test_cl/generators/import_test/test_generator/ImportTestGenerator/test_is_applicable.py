import pytest
from pytest_mock import MockFixture


@pytest.mark.parametrize("is_file, suffix, path, expectation", [
    (False, "", "/home/developer/workspace/src/test_cl", False),
    (True, ".md", "/home/developer/workspace/readme.md", False),
    (True, ".py", "/home/developer/workspace/src/test_cl/__main__.py", False),
    (True, ".py", "/home/developer/workspace/src/test_cl/worker.py", True),
])
def test_happy_scenario(mocker: "MockFixture", is_file, suffix, path, expectation):
    import test_cl.generators.import_test.generator as module

    class FakePath:
        def __init__(self):
            self._is_file = is_file
            self.suffix = suffix
            self._path = path

        def is_file(self):
            return self._is_file

        def __str__(self):
            return self._path

    fake = mocker.Mock(**{
        "source_file.path": FakePath()
    })

    result = module.ImportTestGenerator.is_applicable(
        source_file=fake.source_file,
    )

    assert result == expectation
