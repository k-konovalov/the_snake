"""
Настройки окна/заголовка.
Методы/функции отрисовки объектов на игровой поверхности.
"""

import pygame
from pygame import Surface
from pygame.time import Clock
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, UP, DOWN, LEFT, RIGHT
from game_objects import Apple, Snake, GameObject  # noqa: F401

class PyGameWrapper():
    screen: Surface = ...
    clock: Clock = ...

    def __init__(self):
        # Настройка игрового окна:
        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32
        )
        # Настройка времени:
        self.clock = pygame.time.Clock()

        # Заголовок окна игрового поля:
        pygame.display.set_caption('Змейка')

    def launch(self):
        pygame.init()

    # Функция обработки действий пользователя
    def handle_keys(self, game_object):
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


if __name__ == '__main__':
    print('И зачем? Работает только в составе main())')
    raise Exception('Dummy launch.')
