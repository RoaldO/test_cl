from pathlib import Path

import pytest
from pytest_mock import MockFixture


@pytest.mark.parametrize("project_root, expectation", [
    (Path("/home/dev/ws"), Path("/home/dev/ws/tests")),
])
def test_happy_scenario(mocker: "MockFixture", project_root, expectation):
    import test_cl.generators.whitebox_test.generator as module
    fake = mocker.Mock(**{
        "instance": mocker.Mock(spec=module.WhiteboxTestGenerator, **{
            # class / instance members are faked here
        }),
        "project_root": project_root,
    })

    result = module.WhiteboxTestGenerator._get_tests_root(
        project_root=fake.project_root,
    )

    assert result == expectation
