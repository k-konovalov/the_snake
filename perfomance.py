"""
Performance-декоратор для трекинга времени выполнения тика.

Предоставляет класс PyGamePerfomance со статическим методом measure,
который обёртывает функцию и выводит время её выполнения в миллисекундах.
Используется для мониторинга производительности игрового цикла.
"""
import time
from typing import Any, Callable


class PyGamePerfomance:
    """Класс-контейнер для performance-декоратора."""

    @staticmethod
    def measure(func: Callable) -> Callable:
        """Декоратор для измерения времени выполнения функции.

        Обёртывает переданную функцию, замеряет время выполнения
        с помощью time.perf_counter() и выводит результат в консоль.

        Args:
            func: Функция, время выполнения которой нужно замерить.

        Returns:
            Обёрнутая функция, которая при вызове печатает время
            выполнения и возвращает результат исходной функции.
        """
        def wrapper() -> Any:
            start_time = time.perf_counter()
            result = func()
            end_time = time.perf_counter()

            # Вычисляем разницу в миллисекундах
            elapsed_ms = (end_time - start_time) * 1000

            # Выводим результат
            print(f"Функция {func.__name__} выполнилась за {elapsed_ms:.4f} мс")  # noqa: E501

            return result

        return wrapper(func)
