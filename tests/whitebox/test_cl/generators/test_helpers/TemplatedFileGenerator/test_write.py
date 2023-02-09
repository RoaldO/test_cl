from pytest_mock import MockFixture


# @pytest.mark.parametrize("param_value, expectation", [
#     (0, 0),
#     (1, 1),
#     (2, 2),
# ])
def test_happy_scenario(mocker: "MockFixture"):
    import test_cl.generators.helpers as module
    fake = mocker.Mock(**{
        # mocks go here
    })

    module.TemplatedFileGenerator.write(
        fake.instance,
        output_file=fake.output_file,
        data=fake.data,
    )

