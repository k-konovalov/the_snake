from random import choice, randint  # noqa: F401

from constants import SPEED  # noqa: F401
from pygame_wrapper import PyGameWrapper
from game_objects import Apple, Snake  # noqa: F401


def main():
    # Инициализация PyGame:
    pygame_wrapper = PyGameWrapper()  # noqa: F841
    # Тут нужно создать экземпляры классов.
    apple = Apple()  # noqa: F841
    snake = Snake()  # noqa: F841

    while True:
        # Тут опишите основную логику игры. # noqa: E116
        pygame_wrapper.clock.tick(SPEED)
        pygame_wrapper.handle_keys()


if __name__ == '__main__':
    main()
