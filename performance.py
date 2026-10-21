"""
Performance-декоратор для трекинга времени выполнения тика.

Предоставляет класс PyGamePerformance со статическим методом measure,
который обёртывает функцию и выводит время её выполнения в миллисекундах.
Используется для мониторинга производительности игрового цикла.
"""
import sys
import time


def measure(func):
    """Декоратор для измерения времени выполнения функции.

    Обёртывает переданную функцию, замеряет время выполнения
    с помощью time.perf_counter() и выводит результат в консоль.

    Args:
        func: Функция, время выполнения которой нужно замерить.

    Returns:
        Обёрнутая функция, которая при вызове печатает время
        выполнения и возвращает результат исходной функции.
    """
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()

        # Вычисляем разницу в миллисекундах
        elapsed_ms = (end_time - start_time) * 1000

        # Выводим результат
        sys.stdout.write(
            f'Функция {func.__name__} выполнилась '
            f'за {elapsed_ms:.4f} мс\n',
        )

        return result

    return wrapper


class PyGamePerformance:
    """Класс-контейнер для performance-декоратора."""

    measure = staticmethod(measure)
