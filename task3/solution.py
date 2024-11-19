def get_intervals_overlap(intervals1: list[int],
                          intervals2: list[int]) -> list[int]:
    """
    Находит пересечение двух списков интервалов со временем входа и выхода.

    На вход:
    intervals1 (list[int]): Первый список
    intervals2 (list[int]): Второй список

    Возвращает:
    list[int]: Список интервалов пересечения, показывающий,
    когда оба участника были одновременно.
    """
    overlap = []
    i, j = 0, 0
    while i < len(intervals1) and j < len(intervals2):
        start = max(intervals1[i], intervals2[j])
        end = min(intervals1[i + 1], intervals2[j + 1])
        if start < end:
            if overlap and overlap[-1] >= start:
                overlap[-1] = max(overlap[-1], end)
            else:
                overlap.extend([start, end])

        if intervals1[i + 1] < intervals2[j + 1]:
            i += 2
        else:
            j += 2
    return overlap


def real_lesson_time(intervals: list[int]) -> int:
    """
    Рассчитывает общее время, проведенное в заданных интервалах.

    На вход:
    intervals (list[int]): Список интервалов времени,
    когда на уроке был и учитель, и ученик.

    Возвращает:
    int: Общее время в секундах, проведенное на уроке в указанных интервалах.
    """
    total_time = 0
    for i in range(0, len(intervals), 2):
        total_time += intervals[i + 1] - intervals[i]
    return total_time


def appearance(intervals: dict[str, list[int]]) -> int:
    """
    Рассчитывает общее время присутствия ученика и учителя на уроке.

    На вход:
    intervals (dict[str, list[int]]): Словарь:
        - 'lesson' (list[int]): Время начала и конца урока.
        - 'pupil' (list[int]): Интервалы присутствия ученика.
        - 'tutor' (list[int]): Интервалы присутствия учителя.

    Возвращает:
    int: Время общего присутствия в секундах,
    когда ученик и учитель находились одновременно на уроке.
    """
    pupil_tutor_overlap = get_intervals_overlap(intervals['pupil'],
                                                intervals['tutor'])
    lesson_overlap = get_intervals_overlap(pupil_tutor_overlap,
                                           intervals['lesson'])
    return real_lesson_time(lesson_overlap)


tests = [
    {'intervals': {'lesson': [1594663200, 1594666800],
                   'pupil': [1594663340, 1594663389, 1594663390,
                             1594663395, 1594663396, 1594666472],
                   'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117},
    {'intervals': {'lesson': [1594702800, 1594706400],
                   'pupil': [1594702789, 1594704500, 1594702807, 1594704542,
                             1594704512, 1594704513, 1594704564, 1594705150,
                             1594704581, 1594704582, 1594704734, 1594705009,
                             1594705095, 1594705096, 1594705106, 1594706480,
                             1594705158, 1594705773, 1594705849, 1594706480,
                             1594706500, 1594706875, 1594706502, 1594706503,
                             1594706524, 1594706524, 1594706579, 1594706641],
                   'tutor': [1594700035, 1594700364, 1594702749, 1594705148,
                             1594705149, 1594706463]},
     'answer': 3577},
    {'intervals': {'lesson': [1594692000, 1594695600],
                   'pupil': [1594692033, 1594696347],
                   'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
     'answer': 3565},
]


if __name__ == '__main__':
    for i, test in enumerate(tests):
        test_answer = appearance(test['intervals'])
        assert test_answer == test['answer'], (
            f'Error on test case {i}, got {test_answer}, '
            f'expected {test["answer"]}'
        )
    print("Все тесты прошли успешно!")
