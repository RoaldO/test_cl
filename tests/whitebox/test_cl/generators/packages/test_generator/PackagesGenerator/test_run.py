import pytest
from pytest_mock import MockFixture


@pytest.mark.parametrize("parent_path, source_root", [
    ('/home/dev/ws/', '/home/dev/ws/'),
    ('/home/dev/ws/', '/home/dev/ws/stc/'),
    ('/home/dev/ws/', '/home/dev/ws/stc/tests/'),
])
def test_happy_scenario(mocker: "MockFixture", parent_path, source_root):
    import test_cl.generators.packages.generator as module
    fake = mocker.Mock(**{
        "instance": mocker.Mock(spec=module.PackagesGenerator, **{
            "_template": mocker.Mock(),
        }),
        "source_file": mocker.MagicMock(**{
            "path.parent": parent_path,
            "source_root": source_root,
        }),
    })

    module.PackagesGenerator.run(
        fake.instance,
        source_file=fake.source_file,
    )

    if parent_path == source_root:
        fake.instance.run.assert_not_called()
    else:
        fake.instance.run.assert_called_once()

    fake.instance._template.write.assert_called_once()
