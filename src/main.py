import json
import os

# Количество записей для отображения в виджете
EXECUTED_OPERATIONS_COUNT = 5
ROOT_SRC = 'src'
SRC_FILE = 'operations.json'

if __name__ == "__main__":
    if os.getcwd()[-len(ROOT_SRC):] != ROOT_SRC:
        from src.operation import Operation
    else:
        from operation import Operation

if __name__ == "src.main":
    from src.operation import Operation


def load_operations(file_name):
    """
    Загружает историю банковских операций клиента в список экземпляров класса Operation
    :param file_name: имя файла с историей банковских операций в формате json
    :return: отсортированный список операций по дате
    """
    operation_list = None
    try:
        with open(file_name, mode="r", encoding="utf-8") as file:
            operation_list = json.load(file)
    except IOError:
        if __name__ == "__main__":
            print(f"Ошибка ввода-вывода файла {file_name} с историей операций.")
    # Ошибка при валидации JSON-данных в исходном файле
    except json.decoder.JSONDecodeError:
        if __name__ == "__main__":
            print(f"Ошибка преобразования JSON-данных из файла {file_name}")

    if operation_list is None:
        if __name__ == "__main__":
            print("Ошибка загрузки исходных данных. Программа будет завершена.")
        return

    operations = []
    for item in operation_list:
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
            if __name__ == "__main__":
                print(f'Обнаружена ошибка при загрузке информации о '
                      f'банковской операции в следующей записи файла {file_name}: {item}.')
            continue
        except ValueError:
            if __name__ == "__main__":
                print(f'Обнаружена ошибка при загрузки детализированной информации из файла {file_name} о следующей '
                      f'операции: {item}.')
            continue
    # Сортируем список экземпляров класса Operation по дате операции (по убыванию дат операций -> Operation.date)

    return sorted(operations, key=lambda x: x.date, reverse=True) if operations != [] else []


def filter_operations(operations: list, show_value_cnt: int) -> int:
    """
    Выводит show_value_cnt записей из списка банковских операций, имеющих статус "EXECUTED"
    :param operations: - список экземпляров класса Operation (список всех банковских операций клиента)
    :param show_value_cnt: - количество отображаемых операций для виджета
    :return: количество записей
    """
    count = 0
    for operation in operations:
        if operation.state == "EXECUTED":
            if __name__ == "__main__":
                print(f"{operation.user_report()}\n")
            count += 1
        if count == show_value_cnt:
            break
    # Не найдено ни одной выполненной операции
    if count == 0:
        print('К сожалению не нашлось записей о банковских операциях клиента.')

    return count


def main() -> None:
    """
    Реализация основной бизнес-логики приложения
    :return: None
    """
    # Имя файла для загрузки в зависимости от точки входа программы
    if os.getcwd()[-len(ROOT_SRC):] != ROOT_SRC:
        file_to_load = ROOT_SRC + os.sep + SRC_FILE
    else:
        file_to_load = SRC_FILE
    operations = load_operations(file_to_load)
    if operations is not None:
        print(f'Всего операций данного клиента для анализа: {len(operations)}')
        print(f'Количество последних выполненных операций данного клиента для отображения в виджете: '
              f'{EXECUTED_OPERATIONS_COUNT}\n')
        filter_operations(operations, EXECUTED_OPERATIONS_COUNT)


if __name__ == "__main__":
    main()
