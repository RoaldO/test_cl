from pathlib import Path

import pytest
from pytest_mock import MockFixture


@pytest.mark.parametrize("is_file, suffix, expectation", [
    (True, ".py", True),
    (True, ".pyc", False),
    (False, "", False),
])
def test_happy_scenario(mocker: "MockFixture", is_file, suffix, expectation):
    import test_cl.generators.whitebox_test.generator as module
    from test_cl.simple_types import SourceFile
    fake = mocker.Mock(**{
        "instance": mocker.Mock(spec=module.WhiteboxTestGenerator, **{
            # class / instance members are faked here
        }),
        "source_file": mocker.Mock(spec=SourceFile, **{
            "path": mocker.Mock(**{
                "is_file.return_value": is_file,
                "suffix": suffix,
            })
        })
    })

    result = module.WhiteboxTestGenerator.is_applicable(
        source_file=fake.source_file,
    )

    assert result is expectation
