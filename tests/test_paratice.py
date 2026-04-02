import pytest

@pytest.fixture()
def setup():
    print("this method run first")

@pytest.mark.smoke
def test_wer(setup):
    print("after fixture this method cala")
@pytest.mark.regression
def test_wer2(setup):
    print("after fixture this method cala")