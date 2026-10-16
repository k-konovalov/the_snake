from random import choice, randint  # noqa: F401

from constants import SCREEN_WIDTH, SCREEN_HEIGHT  # noqa: F401
from pygame_wrapper import PyGameWrapper
from game_objects import GameObject, Apple, Snake  # noqa: F401


def main():
    # Инициализация PyGame:
    pygame_wrapper = PyGameWrapper()  # noqa: F841
    # Тут нужно создать экземпляры классов.
    ...

    # while True:
    #     clock.tick(SPEED)

        # Тут опишите основную логику игры. # noqa: E116
        # ...  # noqa: E116


if __name__ == '__main__':
    main()


# Метод draw класса Apple
# def draw(self):
#     rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, rect)
#     pygame.draw.rect(screen, BORDER_COLOR, rect, 1)



# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None
