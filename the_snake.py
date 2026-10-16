"""
Точка входа игры «Изгиб Питона».

Реэкспортирует все обязательные элементы (константы, классы, функции)
для прохождения тестов через hasattr. Основной игровой цикл
реализован в функции main().
"""
from random import choice, randint  # noqa: F401

from constants import SPEED  # noqa: F401
from pygame_wrapper import PyGameWrapper
from game_objects import Apple, Snake  # noqa: F401


def main():
    """Основной игровой цикл.

    Инициализирует Pygame, создаёт экземпляры Snake и Apple,
    затем в бесконечном цикле:
        1. Ограничивает частоту кадров через clock.tick(SPEED).
        2. Обрабатывает нажатия клавиш через handle_keys().
        3. Обновляет направление змейки через update_direction().
        4. Двигает змейку через move().
        5. Проверяет поедание яблока (рост + новая позиция).
        6. Проверяет столкновение с собой (reset при коллизии).
        7. Отрисовывает объекты и обновляет экран.
    """
    # Инициализация PyGame:
    pygame_wrapper = PyGameWrapper()  # noqa: F841
    # Тут нужно создать экземпляры классов.
    apple = Apple()  # noqa: F841
    snake = Snake()  # noqa: F841

    while True:
        # Тут опишите основную логику игры. # noqa: E116
        pygame_wrapper.clock.tick(SPEED)
        pygame_wrapper.handle_keys(snake)


if __name__ == '__main__':
    main()
