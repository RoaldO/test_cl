from pytest_mock import MockFixture


# @pytest.mark.parametrize("param_value, expectation", [
#     (0, 0),
#     (1, 1),
#     (2, 2),
# ])
def test_happy_scenario(mocker: "MockFixture"):
    import test_cl.generators.import_test.generator as module
    from test_cl.simple_types import Module

    class FakePath:
        def __truediv__(self, other):
            return FakePath()

        @property
        def parent(self):
            return FakePath()

    fake = mocker.Mock(**{
        "PackagesGenerator": mocker.patch("test_cl.generators.import_test.generator.PackagesGenerator"),
        "source_file.project_root": FakePath(),
        "source_file.path": FakePath(),
        "source_file.identifier": Module("a.b.c"),
    })

    module.ImportTestGenerator.run(
        fake.instance,
        source_file=fake.source_file,
    )

    fake.PackagesGenerator.return_value.run.assert_called_once()
    fake.instance._template.write.assert_called_once()
