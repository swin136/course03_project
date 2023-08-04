import json
from operation import Operation

# Количество записей для отображения в виджете
EXECUTED_OPERATIONS_COUNT = 5
SRC_FILE = 'operations.json'


def load_operations(file_name):
    """
    Загружает историю банковских операций клиента в список экземпляров класса Operation
    :param file_name: имя файла с историей банковских операций в формате json
    :return:
    """
    operation_list = None
    try:
        with open(file_name, mode="r", encoding="utf-8") as file:
            operation_list = json.load(file)
    except IOError:
        print(f"Ошибка ввода-вывода файла {file_name} с историей операций.")
    # Ошибка при валидации JSON-данных в исходном файле
    except json.decoder.JSONDecodeError:
        print(f"Ошибка преобразования JSON-данных из файла {file_name}")

    if operation_list is None:
        print("Ошибка загрузки исходных данных. Программа будет завершена.")
        return

    operations = []
    for item in operation_list:
        # print(item)
        from_ = item.get('from')
        if from_ is None:
            from_ = ""
        try:
            operation = Operation(operation_id=item['id'],
                                  date=item['date'],
                                  state=item['state'],
                                  operation_amount=item['operationAmount'],
                                  description=item['description'],
                                  from_=from_,
                                  to_=item['to']
                                  )
            operations.append(operation)
        except KeyError:
            print(f'Обнаружена ошибка при загрузке информации о '
                  f'банковской операции в следующей записи файла {file_name}: {item}.')
            continue
        except ValueError:
            print(f'Обнаружена ошибка при загрузки детализированной информации из файла {file_name} о следующей '
                  f'операции: {item}.')
            continue
    # Сортируем список экземпляров класса Operation по дате операции (по убыванию дат операций -> Operation.date)
    return sorted(operations, key=lambda x: x.date, reverse=True)


def filter_operations(operations: list, show_value_cnt: int) -> None:
    """
    Выводит show_value_cnt записей из списка банковских операций, имеющих статус "EXECUTED"
    :param operations: - список экземпляров класса Operation (список всех банковских операций клиента)
    :param show_value_cnt: - количество отображаемых операций для виджета
    :return: None
    """
    count = 0
    for operation in operations:
        if operation.state == "EXECUTED":
            # print(operation)
            print(f"{operation.user_report()}\n")
            count += 1
        if count == show_value_cnt:
            break
    # Не найдено ни одной выполненной операции
    if count == 0:
        print('К сожалению не нашлось записей о банковских операциях клиента.')


def main() -> None:
    """
    Реализация основной бизнес-логики приложения
    :return: None
    """
    operations = load_operations(SRC_FILE)
    if operations is not None:
        print(f'Всего операций данного клиента для анализа: {len(operations)}')
        print(f'Количество последних выполненных операций данного клиента для отображения в виджете: '
              f'{EXECUTED_OPERATIONS_COUNT}\n')
        filter_operations(operations, EXECUTED_OPERATIONS_COUNT)


if __name__ == "__main__":
    main()
