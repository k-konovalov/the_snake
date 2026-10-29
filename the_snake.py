"""
Точка входа игры «Изгиб Питона».

Реэкспортирует все обязательные элементы (константы, классы, функции)
для прохождения тестов через hasattr. Основной игровой цикл
реализован в функции main().
"""

import pygame

from constants import (BOARD_BACKGROUND_COLOR, DOWN, GRID_HEIGHT, GRID_SIZE,
                       GRID_WIDTH, LEFT, RIGHT, SCREEN_HEIGHT, SCREEN_WIDTH,
                       SPEED, UP)
from game_objects import Apple, GameObject, Snake

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

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


def handle_keys(game_object):
    """Обрабатывает события клавиатуры для смены направления змейки.

    Обработает события QUIT (закрытие окна) и KEYDOWN (нажатие
    стрелок). Запрещает разворот змейки на 180 градусов.

    Args:
        game_object: Объект Snake, направление которого нужно изменить.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            key = event.key
            if key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


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
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple(restricted_positions=snake.positions)

    while True:
        # Тут опишите основную логику игры.
        clock.tick(SPEED)
        handle_keys(snake)
        screen.fill(BOARD_BACKGROUND_COLOR)

        snake.update_direction()
        snake.move(field_size=(SCREEN_WIDTH, SCREEN_HEIGHT))

        if snake.position == apple.position:
            snake.length = len(snake.positions)
            apple.randomize_position(restricted_positions=snake.positions)
        else:
            snake.positions.pop()

        snake.eat_snake(func_clear=screen.fill(BOARD_BACKGROUND_COLOR))
        apple.draw(screen)
        snake.draw(screen)

        pygame.display.flip()


if __name__ == '__main__':
    main()
