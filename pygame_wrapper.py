"""
Обёртка над Pygame: настройка окна, заголовка и обработка событий.

Предоставляет класс PyGameWrapper, который инициализирует игровое
окно размером 640x480, устанавливает заголовок и предоставляет
методы для обработки нажатий клавиш и работы с таймингом.
"""

import pygame
from pygame import Surface
from pygame.time import Clock

from constants import (BOARD_BACKGROUND_COLOR, DOWN, LEFT, RIGHT,
                       SCREEN_HEIGHT, SCREEN_WIDTH, UP)


class PyGameWrapper:
    """Обёртка для управления окном Pygame и обработки ввода.

    Атрибуты:
        screen: Surface — поверхность pygame для отрисовки игрового поля.
        clock: Clock — таймер pygame для контроля частоты кадров.
    """

    screen: Surface = ...
    clock: Clock = ...

    def __init__(self):
        """Инициализирует игровое окно и таймер.

        Создаёт окно размером SCREEN_WIDTH x SCREEN_HEIGHT,
        устанавливает заголовок «Змейка» и создаёт объект Clock
        для контроля FPS.
        """
        # Настройка игрового окна:
        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32,
        )
        # Настройка времени:
        self.clock = pygame.time.Clock()

        # Заголовок окна игрового поля:
        pygame.display.set_caption('Змейка')

    def launch(self):
        """Инициализирует подсистемы Pygame.

        Вызывает pygame.init() для подготовки всех модулей.
        """
        pygame.init()

    def handle_keys(self, game_object):
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

    def flip(self):
        """Запрос на отрисовку"""
        pygame.display.flip()

    def clear(self):
        """Очищение игрового поля"""
        self.screen.fill(BOARD_BACKGROUND_COLOR)


if __name__ == '__main__':
    raise Exception('Dummy launch.')
