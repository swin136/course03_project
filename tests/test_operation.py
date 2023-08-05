import pytest
import datetime
from src.operation import masquerade_account
from src.operation import Operation


@pytest.mark.parametrize('input_account, masq_account',
                         [
                             ('Maestro 1596837868705199', 'Maestro 1596 83** **** 5199'),
                             ('Счет 64686473678894779589', 'Счет **9589'),
                             ('MasterCard 7158300734726758', 'MasterCard 7158 30** **** 6758'),
                             ('Visa Classic 6831982476737658', 'Visa Classic 6831 98** **** 7658')
                         ]
                         )

def test_masquerade_account(input_account, masq_account):
    assert masquerade_account(input_account) == masq_account


# # Буквы в номере карты, счета
# @pytest.mark.parametrize('non_digit_account',
#                          [
#                              'Maestro 15968378687051xx',
#                              'Счет xx686473678894779589',
#                              'Visa Classic 683198247673D6C8'
#
#                          ]
#                          )
# def test_non_digit_account(non_digit_account):
#     with pytest.raises(ValueError):
#         masquerade_account(non_digit_account)

# Длина банковоской карты не равна 16 цифрам
@pytest.mark.parametrize('illegal_account',
                         [
                             'Maestro 15968378687051121',
                             'Visa Classic 683198247673'
                         ]
                         )
def test_illegal_length_account(illegal_account):
    with pytest.raises(ValueError):
        masquerade_account(illegal_account)

# Тестируем наш основной класс
@pytest.fixture
def get_inst_class():
    operation = Operation(
    operation_id=873106923,
    description="Перевод со счета на счет",
    state='EXECUTED',
    date='2019-03-23T01:09:46.296404',
    to_='Счет 74489636417521191160',
    from_='Счет 44812258784861134719',
    operation_amount={
        "amount": "43318.34",
        "currency": {
                    "name": "руб.",
                    "code": "RUB"
                    }
   }
    )
    return operation

@pytest.fixture
def get_inst_class_wo_from():
    operation = Operation(
    operation_id=596171168,
    description="Открытие вклада",
    state='EXECUTED',
    date='2018-07-11T02:26:18.671407',
    to_='Счет 72082042523231456215',
    operation_amount={
        "amount": "79931.03",
        "currency": {
                    "name": "руб.",
                    "code": "RUB"
                    }
   }
    )
    return operation

def test_class_init(get_inst_class):
    assert get_inst_class.state == 'EXECUTED'
    assert get_inst_class.date == datetime.datetime(2019, 3, 23, 1, 9, 46, 296404)
    assert get_inst_class.user_report() == ("23.03.2019\n"
                                       "Перевод со счета на счет\n"
                                       "Счет **4719 -> Счет **1160\n"
                                       "43318.34 руб.")

def test_class_wo_from_init(get_inst_class_wo_from):
    assert get_inst_class_wo_from.state == 'EXECUTED'
    assert get_inst_class_wo_from.date == datetime.datetime(2018, 7, 11,2, 26, 18, 671407)
    assert get_inst_class_wo_from.user_report() == ("11.07.2018\n"
                                            "Открытие вклада\n"
                                            "Счет **6215\n"
                                            "79931.03 руб.")

#
def test_illegel_bank_account():
#     # Класс с номером карты, в котором нет 16 цифр
    with pytest.raises(ValueError):
        operation = Operation(
            operation_id=596171168,
            description="Открытие вклада",
            state='EXECUTED',
            date='2018-07-11T02:26:18.671407',
            to_='Maestro 12345',
            operation_amount={
                "amount": "79931.03",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            }
        )
#
def test_illegel_bank_account2():
   # Операция с ноиером счета, в котором менее 6 цифр
    with pytest.raises(ValueError):
        operation = Operation(
            operation_id=596171168,
            description="Открытие вклада",
            state='EXECUTED',
            date='2018-07-11T02:26:18.671407',
            to_='Счет 8416',
            operation_amount={
                "amount": "79931.03",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            }
        )


