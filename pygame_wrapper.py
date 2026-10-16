"""
Обёртка над Pygame: настройка окна, заголовка и обработка событий.

Предоставляет класс PyGameWrapper, который инициализирует игровое
окно размером 640x480, устанавливает заголовок и предоставляет
методы для обработки нажатий клавиш и работы с таймингом.
"""

import pygame
from pygame import Surface
from pygame.time import Clock
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, UP, DOWN, LEFT, RIGHT, BOARD_BACKGROUND_COLOR
from game_objects import Apple, Snake, GameObject  # noqa: F401


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
                if event.key == pygame.K_UP and game_object.direction != DOWN:
                    game_object.next_direction = UP
                elif event.key == pygame.K_DOWN and game_object.direction != UP:  # noqa: E501
                    game_object.next_direction = DOWN
                elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:  # noqa: E501
                    game_object.next_direction = LEFT
                elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:  # noqa: E501
                    game_object.next_direction = RIGHT

    def clear(self):
        """Очищение игрового поля"""
        self.screen.fill(BOARD_BACKGROUND_COLOR)


if __name__ == '__main__':
    print('И зачем? Работает только в составе main())')
    raise Exception('Dummy launch.')
