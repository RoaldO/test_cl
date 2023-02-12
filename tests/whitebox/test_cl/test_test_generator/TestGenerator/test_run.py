from unittest.mock import call

from pytest_mock import MockFixture


def test_happy_scenario(mocker: "MockFixture"):
    import test_cl.test_generator as module
    fake = mocker.Mock(**{
        "instance": mocker.Mock(spec=module.TestGenerator, **{
            "get_source_files": mocker.Mock(**{
                "return_value": [
                    (fake_source_file_1 := mocker.Mock()),
                    (fake_source_file_2 := mocker.Mock()),
                    (fake_source_file_3 := mocker.Mock()),
                ]
            })
        })
    })

    module.TestGenerator.run(
        fake.instance,
    )

    fake.instance.get_source_files.assert_called_once()
    fake.instance.generate_resources.assert_has_calls([
        call(fake_source_file_1),
        call(fake_source_file_2),
        call(fake_source_file_3),
    ])
