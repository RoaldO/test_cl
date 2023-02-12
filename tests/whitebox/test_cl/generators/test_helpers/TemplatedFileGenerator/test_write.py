from pathlib import Path
from unittest.mock import ANY

import pytest
from pytest_mock import MockFixture


# @pytest.mark.parametrize("param_value, expectation", [
#     (0, 0),
#     (1, 1),
#     (2, 2),
# ])
def test_happy_scenario(mocker: "MockFixture"):
    import test_cl.generators.helpers as module

    fake = mocker.Mock(**{
        "instance": mocker.Mock(spec=module.TemplatedFileGenerator, **{
            "_template": mocker.Mock(**{
                "render.return_value": "fake_string",
            }),
        }),
    })

    module.TemplatedFileGenerator.write(
        fake.instance,
        output_file=fake.output_file,
        data=fake.data,
        end_with_newline=fake.end_with_newline,
    )

    fake.instance._template.render.assert_called_once_with(
        run={
            'now': ANY,
            'login': ANY,
        },
        data=fake.data,
    )
    fake.output_file.path.parent.mkdir.assert_called_once_with(
        parents=True,
        exist_ok=True,
    )
    fake.output_file.path.exists.assert_called_once()
