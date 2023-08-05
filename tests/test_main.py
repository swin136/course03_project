from src.main import load_operations


def test_load():
    assert load_operations('no_file') == None