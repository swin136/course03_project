import datetime


def masquerade_account(account: str) -> str:
    """
    Вспомогательная функция - маскирует часть цифр номера банковской карты (счета)
    :param account: строка с типом счета(карты) и номером
    :return: строка с типом счета(карты) и замаскированным номером
    """
    account_list = account.split()
    # Получаем строку с номером счета/банковской карты
    num_account = account_list[len(account_list) - 1]
    if account_list[0] == 'Счет':
        # Преобразуем номер счета.
        # Маскируем номер счета в формате  **XXXX - 6 символов: ** плюс последние 4 цифры номера
        show_account_num = "Счет " + "*" * 2 + num_account[-4:]

    else:
        # Преобразуем номер банковской карты
        # Преобразуем номер карты в формат  XXXX XX** **** XXXX
        show_account_num = num_account[:4] + " " + num_account[4:6] + "*" * 2 + " " + "*" * 4 + " " + num_account[-4:]
        # удаляем из списка полный номер карты и подставляем вместо него
        account_list.pop()
        account_list.append(show_account_num)
        show_account_num = " ".join(account_list)

    return show_account_num


class Operation:
    def __init__(self, operation_id: int, state: str, date: str,
                 operation_amount: dict, description: str, to_: str, from_=""):
        self.__id = operation_id
        self.__description = description.strip()
        self.__from = from_.strip()
        self.__to = to_.strip()
        if not self.validate_account('to'):
            raise ValueError
        if self.__from != "":
            if not self.validate_account('from'):
                raise ValueError

        # Проверяем поле state
        test_state = state.upper().strip()
        if test_state not in ("EXECUTED", "CANCELED"):
            raise ValueError
        self.__state = test_state

        # Проверяем поле operationAmount
        if operation_amount.get('amount') is None:
            raise ValueError
        if operation_amount.get('currency') is None:
            raise ValueError
        else:
            if operation_amount.get('currency').get('name') is None \
                    or operation_amount.get('currency').get('code') is None:
                raise ValueError
        self.__operationAmount = operation_amount
        # Работаем с полем date - тип datetime
        self.__date = datetime.datetime.fromisoformat(date)

    def get_date(self):
        return self.__date

    def get_state(self):
        return self.__state

    date = property(get_date)
    state = property(get_state)

    def __repr__(self):
        return f"Банковская операция: транзакция №{self.__id}, дата: {self.__date.strftime('%d.%m.%Y')}, " \
               f"статус операции: {self.__state}, сумма операции: {self.__operationAmount['amount']} " \
               f"{self.__operationAmount['currency']['name']}"

    def validate_account(self, test_account: str) -> bool:
        """
        Проверяет корректность номера счета/карты.
        В номере банковской карты должно быть 16 цифр.
        В номере банковского счета должно быть не менее 6 цифр.
        :param test_account:
        :return:
        """
        match test_account:
            case 'from':
                account = self.__from
            case 'to':
                account = self.__to
        account_list = account.split()
        # Получаем строку с номером счета/банковской карты
        num_account = account_list[len(account_list) - 1]
        if not num_account.isdigit():
            return False
        # Цифр в номере счета больше 6
        if account_list[0] == 'Счет':
            if len(num_account) < 6:
                return False
        else:
            # Цифр в номере банковской карты не 16
            if len(num_account) != 16:
                return False
        return True

    def user_report(self) -> str:
        """
        Вывод строк с параметрами банковской операции для отображения в виджете в формате
        <дата перевода> <описание перевода>
        <откуда> -> <куда>
        <сумма перевода> <валюта>
        :return:
        """
        out_str = f"{self.__date.strftime('%d.%m.%Y')}\n" \
                  f"{self.__description}\n"
        if self.__from != "":
            out_str = out_str + masquerade_account(self.__from) + " -> " + masquerade_account(self.__to) + "\n"
        else:
            out_str = out_str + masquerade_account(self.__to) + "\n"
        out_str = out_str + f"{self.__operationAmount['amount']} {self.__operationAmount['currency']['name']}"

        return out_str
