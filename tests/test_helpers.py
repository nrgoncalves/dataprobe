from dataprobe.helpers import flatten_list


class TestHelpers(object):
    def test_flatten_list(self):
        x = [[], 1, ['astring', 1, 'anotherone']]
        assert flatten_list(x) == [1, 'astring', 1, 'anotherone']

    def test_flatten_empty_list(self):
        x = []
        assert flatten_list(x) == []

    def test_flatten_empty_list_nested(self):
        x = [[], [], []]
        assert flatten_list(x) == []
