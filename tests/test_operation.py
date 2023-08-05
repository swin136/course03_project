import pytest
import datetime
from src.operation import masquerade_account
from src.operation import Operation


@pytest.mark.parametrize('input_account, masq_account',
                         [
                             ('Maestro 1596837868705199', 'Maestro 1596 83** **** 5199'),
                             ('Счет 64686473678894779589', 'Счет **9589'),
                             ('MasterCard 7158300734726758', 'MasterCard 7158 30** **** 6758'),
                             ('Visa Classic 6831982476737658', 'Visa Classic 6831 98** **** 7658'),
                             ('МИР 1234876590096787', 'МИР 1234 87** **** 6787')
                         ]
                         )

def test_masquerade_account(input_account, masq_account):
    assert masquerade_account(input_account) == masq_account

# Тестируем наш основной класс c правильными значениями полей
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

def test_class_init(get_inst_class):
    assert get_inst_class.state == 'EXECUTED'
    assert get_inst_class.date == datetime.datetime(2019, 3, 23, 1, 9, 46, 296404)
    assert get_inst_class.user_report() == ("23.03.2019\n"
                                       "Перевод со счета на счет\n"
                                       "Счет **4719 -> Счет **1160\n"
                                       "43318.34 руб.")


    assert str(get_inst_class) == 'Банковская операция: транзакция №873106923, дата: 23.03.2019, статус операции: EXECUTED, сумма операции: 43318.34 руб.'

# Тестируем наш основной класс, при инициализации которого значение поля "from" пустое
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



def test_class_wo_from_init(get_inst_class_wo_from):
    assert get_inst_class_wo_from.state == 'EXECUTED'
    assert get_inst_class_wo_from.date == datetime.datetime(2018, 7, 11,2, 26, 18, 671407)
    assert get_inst_class_wo_from.user_report() == ("11.07.2018\n"
                                            "Открытие вклада\n"
                                            "Счет **6215\n"
                                            "79931.03 руб.")

    assert str(get_inst_class_wo_from) == ('Банковская операция: транзакция №596171168, '
                                           'дата: 11.07.2018, статус операции: EXECUTED, сумма операции: 79931.03 руб.')

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
   # Тестируем загрузку информации об операции в номиере счета, в котором менее 6 цифр
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


def test_illegel_bank_account3():
   # Тестируем загрузку информации об операции в номере счета, в котором менее 6 цифр
   #  to_='Счет 12345'
    with pytest.raises(ValueError):
        operation = Operation(
            operation_id=596171168,
            description="Открытие вклада",
            state='EXECUTED',
            date='2018-07-11T02:26:18.671407',
            to_='Счет 12345',
            operation_amount={
                "amount": "79931.03",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            }
        )

def test_illegel_bank_account4():
    # Тестируем загрузку информации об операции в номере счета получателя имеются буквы
    # to_='MasterCard 71583007347267XX',
    with pytest.raises(ValueError):
        operation = Operation(
            operation_id=873106923,
            description="Перевод со счета на счет",
            state='EXECUTED',
            date='2019-03-23T01:09:46.296404',
            to_='MasterCard 71583007347267XX',
            from_='Счет 44812258784861134719',
            operation_amount={
                "amount": "43318.34",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            }
        )

def test_opearation_illegal_state():
    # Тестируем загрузку информации об операции в номере счета получателя имеются буквы
    # to_='MasterCard 71583007347267XX',
    with pytest.raises(ValueError):
        operation = Operation(
            operation_id=873106923,
            description="Перевод со счета на счет",
            state='EXECUTED1',
            date='2019-03-23T01:09:46.296404',
            to_='MasterCard 7158300734726711',
            from_='Счет 44812258784861134719',
            operation_amount={
                "amount": "43318.34",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            }
        )

def test_no_currensy():
    with pytest.raises(ValueError):
        operation = Operation(
            operation_id=873106923,
            description="Перевод со счета на счет",
            state='EXECUTED',
            date='2019-03-23T01:09:46.296404',
            to_='MasterCard 7158300734726711',
            from_='Счет 44812258784861134719',
            operation_amount={
                "amount": "43318.34",
                "currency1": {
                    "name": "руб.",
                    "code": "RUB"
                }
            }
        )

def test_no_amount():
    with pytest.raises(ValueError):
        operation = Operation(
            operation_id=873106923,
            description="Перевод со счета на счет",
            state='EXECUTED',
            date='2019-03-23T01:09:46.296404',
            to_='MasterCard 7158300734726711',
            from_='Счет 44812258784861134719',
            operation_amount={
                "amount_error": "43318.34",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            }
        )

def test_no_currency_name():
    with pytest.raises(ValueError):
        operation = Operation(
            operation_id=873106923,
            description="Перевод со счета на счет",
            state='EXECUTED',
            date='2019-03-23T01:09:46.296404',
            to_='MasterCard 7158300734726712',
            from_='Счет 44812258784861134719',
            operation_amount={
                "amount": "43318.34",
                "currency": {
                    "name_error": "руб.",
                    "code": "RUB"
                }
            }
        )
