import pytest


@pytest.mark.parametrize("n,expected", [(1, 2), (3, 5)])
class TestParatice:

    def test(self,n,expected):
        assert  n + 1== expected