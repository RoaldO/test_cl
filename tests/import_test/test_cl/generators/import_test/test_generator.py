"""
test generated on 2023-01-26 19:44:03.656109 by roald
"""


def test_module_can_be_imported():
    """ it is always a good idea to test if every module can be tested """
    import test_cl.generators.import_test.generator as module
    assert module is not None