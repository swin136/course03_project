import pytest
import os
from src.main import load_operations
from src.main import filter_operations


# Точка входа при запуске тестирования из PyCharm и из корня проекта
@pytest.fixture
def get_root_dir():
    root_tests = 'tests'
    """
    При запуске тестов из PyCharm возврат функции должен быть: return ""
    При запуске тестов из терминала в корне проекта возврат функции должен быть: return "tests\\" или return "tests\\"
    """
    if os.getcwd()[-len(root_tests):] != root_tests:
        tests_to_load = root_tests + os.sep
    else:
        tests_to_load = ''
    return tests_to_load


def test_load_no_file():
    assert load_operations('no_file') is None


def test_load_error_json(get_root_dir):
    assert load_operations(get_root_dir + 'operations_error.json') is None


def test_load_normal_json(get_root_dir):
    test_list = load_operations(get_root_dir + 'operations_main.json')
    assert len(test_list) == 100
    assert filter_operations(test_list, 5) == 5
    assert len(load_operations(get_root_dir + 'operations_errors_2.json')) == 98


def test_load_empty(get_root_dir):
    assert load_operations(get_root_dir + 'empty.json') == []
