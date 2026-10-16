"""
Классы игровых объектов.
"""

import pygame
from pygame import Rect, Surface
from constants import GRID_HEIGHT, GRID_SIZE, BORDER_COLOR, BOARD_BACKGROUND_COLOR


class GameObject:
    position = ...
    positions: list[int] = ...
    body_color = ...
    
    def __init__(self, position, body_color):
        self.position = position
        self.body_color = body_color

    def draw(self, screen: Surface):
        pass


class Apple(GameObject):
    def randomize_position(self):
        """
        случайные координаты в пределах поля
        """
        pass

    # Метод draw класса Apple
    def draw(self, screen: Surface):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    next_direction = ...
    length = ...
    last: pygame.Rect = ...

    def get_head_position(self):
        pass

    def move(self):
        pass

    def reset(self):
        pass

    def update_direction(self):
        """
        Метод обновления направления после нажатия на кнопку
        """
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self, screen: Surface):
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


if __name__ == '__main__':
    print('И зачем? Работает только в составе main())')
    raise Exception('Dummy launch.')
