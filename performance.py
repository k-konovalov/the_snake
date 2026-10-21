"""
Performance-декоратор для трекинга времени выполнения тика.

Предоставляет класс PyGamePerformance со статическим методом measure,
который обёртывает функцию и выводит время её выполнения в миллисекундах.
Используется для мониторинга производительности игрового цикла.
"""
import time


class PyGamePerformance:
    """Класс-контейнер для performance-декоратора."""

    @staticmethod
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
            print(f"Функция {func.__name__} выполнилась за {elapsed_ms:.4f} мс")  # noqa: E501

            return result

        return wrapper
