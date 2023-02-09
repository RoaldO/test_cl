from pathlib import Path, PosixPath

import pytest
from pytest_mock import MockFixture


@pytest.mark.parametrize("project_root, source_root, source_file, test_source_root, expectation", [
    (
            "/home/dev/project/",
            "/home/dev/project/src/",
            "/home/dev/project/src/package/file.py",
            "/home/dev/project/tests/",
            "/home/dev/project/tests/imports/package/test_file.py",
    ),
])
def test_happy_scenario(mocker: "MockFixture", project_root, source_root, source_file, test_source_root, expectation):
    import test_cl.generators.import_test.generator as module
    from test_cl.simple_types import SourceFile

    class FakePath(PosixPath):
        def is_file(self) -> bool:
            return True

    fake = mocker.Mock(**{
        # mocks go here
        "source_root": Path(test_source_root),
        "source_file": SourceFile(
            project_root=Path(project_root),
            source_root=Path(source_root),
            path=FakePath(source_file),
        ),
    })

    result = module.ImportTestGenerator._get_test_source_path(
        source_file=fake.source_file,
        source_root=fake.source_root,
    )

    assert result == Path(expectation)
