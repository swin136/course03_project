from src.main import load_operations
from src.main import filter_operations


def test_load_no_file():
    assert load_operations('no_file') == None

def test_load_error_json():
    assert load_operations('tests/operations_error.json') == None

def test_load_normal_json():
    test_list = load_operations('tests/operations_main.json')
    assert len(test_list) == 100
    assert filter_operations(test_list, 5) == 5
    # assert len(load_operations('tests/operations_err_record.json')) == 99

def test_load_empty():
    assert load_operations('tests/empty.json') == []

