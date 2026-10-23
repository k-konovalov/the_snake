"""
Точка входа игры «Изгиб Питона».

Реэкспортирует все обязательные элементы (константы, классы, функции)
для прохождения тестов через hasattr. Основной игровой цикл
реализован в функции main().
"""

from constants import (BOARD_BACKGROUND_COLOR, DOWN, GRID_HEIGHT, GRID_SIZE,
                       GRID_WIDTH, LEFT, RIGHT, SCREEN_HEIGHT, SCREEN_WIDTH,
                       SPEED, UP)
from game_objects import Apple, GameObject, Snake
from pygame_wrapper import PyGameWrapper

__all__ = [
    'Apple',
    'BOARD_BACKGROUND_COLOR',
    'DOWN',
    'GameObject',
    'GRID_HEIGHT',
    'GRID_SIZE',
    'GRID_WIDTH',
    'LEFT',
    'RIGHT',
    'SCREEN_HEIGHT',
    'SCREEN_WIDTH',
    'Snake',
    'SPEED',
    'UP',
]


def handle_keys(game_object):
    """Заглушка для тестов см. PyGameWrapper"""


def main():
    """Основной игровой цикл.

    Инициализирует Pygame, создаёт экземпляры Snake и Apple,
    затем в бесконечном цикле:
        1. Ограничивает частоту кадров через pygame_wrapper.clock.tick(SPEED).
        2. Обрабатывает нажатия клавиш через handle_keys().
        3. Обновляет направление змейки через update_direction().
        4. Двигает змейку через move().
        5. Проверяет поедание яблока (рост + новая позиция).
        6. Проверяет столкновение с собой (reset при коллизии).
        7. Отрисовывает объекты и обновляет экран.
    """
    # Инициализация PyGame:
    pygame_wrapper = PyGameWrapper()
    pygame_wrapper.launch()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple(restricted_positions=snake.positions)

    while True:
        # Тут опишите основную логику игры.
        pygame_wrapper.clock.tick(SPEED)
        pygame_wrapper.handle_keys(snake)
        pygame_wrapper.clear()

        snake.update_direction()
        snake.move(field_size=(SCREEN_WIDTH, SCREEN_HEIGHT))

        if snake.position == apple.position:
            snake.length = len(snake.positions)
            apple.randomize_position(restricted_positions=snake.positions)
        else:
            snake.positions.pop()

        snake.eat_snake(func_clear=pygame_wrapper.clear)
        apple.draw(pygame_wrapper.screen)
        snake.draw(pygame_wrapper.screen)

        pygame_wrapper.flip()


if __name__ == '__main__':
    main()
