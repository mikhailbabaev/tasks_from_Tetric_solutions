def strict(func):
    """
    Декоратор для проверки типов аргументов функции.

    Для каждого аргумента, передаваемого в функцию, проверяется,
    соответствует ли его тип указанному в аннотации.

    """
    def wrapper(*args, **kwargs):
        annotations = func.__annotations__
        for param_name, expected_type in annotations.items():
            if param_name == 'return':
                continue
            if param_name in kwargs:
                arg_value = kwargs[param_name]
            else:
                i = func.__code__.co_varnames.index(param_name)
                arg_value = args[i]
            if not isinstance(arg_value, expected_type):
                raise TypeError(
                    f'Аргумент {param_name} должен быть '
                    f'{expected_type.__name__}. '
                    f'Получен тип {type(arg_value).__name__}.'
                    )
        return func(*args, **kwargs)
    return wrapper


@strict
def test_function(a: bool, b: int, c: float, d: str) -> str:
    """Функция для теста декоратора.

    На вход:
        a (bool): булев параметр
        b (int): целочисленный параметр
        c (float): число с плавающей точкой
        d (str): строка

    Возвращает:
        str: строку
    """
    return f'{a}, {b}, {c}, {d}'


test_cases = [
    (True, 5, 3.14, 'Hello'),
    (True, 5.5, 3.14, "Hello"),
    (1, 5, 3.14, "Hello"),
    (True, 5, "str", "Hello"),
    (True, 5, 3.14, 123)
]

for i, test_case in enumerate(test_cases):
    try:
        n = i + 1
        result = test_function(*test_case)
        print(f"Test {n}: {result} - Passed")
    except TypeError as e:
        print(f"Test {n}: Failed with error: {e}")
