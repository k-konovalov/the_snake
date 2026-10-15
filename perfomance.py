"""
Performance-декоратор для трекинга времени выполнения тика
"""
import time


class PyGamePerfomance():
    @staticmethod
    def measure(func):
        def wrapper():
            start_time = time.perf_counter()
            result = func()
            end_time = time.perf_counter()

            # Вычисляем разницу в миллисекундах
            elapsed_ms = (end_time - start_time) * 1000

            # Выводим результат
            print(f"Функция {func.__name__} выполнилась за {elapsed_ms:.4f} мс")  # noqa: E501

            return result

        return wrapper(func)
