from pytest_mock import MockFixture


def test_happy_scenario(mocker: "MockFixture", source_example):
    import test_cl.helpers as module
    fake = mocker.Mock(**{
        "instance": mocker.Mock(spec=module.AstWrapper, **{
            "source_file": mocker.Mock(**{
                "path": mocker.MagicMock(**{
                    "read_text.return_value": source_example,
                }),
            }),
            "iter_classes": mocker.Mock(**{
                "return_value": [],
            }),
        }),
        "node": None,
    })

    result = list(module.AstWrapper.iter_classes(
        fake.instance,
        node=fake.node,
    ))

    assert len(result) == 2
