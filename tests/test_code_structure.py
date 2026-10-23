import pygame
import pytest
import constants


EXPECTED_GAME_OBJECT_ATTRS = (
    ('атрибут', 'position'),
    ('атрибут', 'body_color'),
    ('метод', 'draw'),
)


@pytest.mark.parametrize(
    'attr_type, attr_name',
    EXPECTED_GAME_OBJECT_ATTRS,
    ids=[elem[1] for elem in EXPECTED_GAME_OBJECT_ATTRS]
)
def test_game_object_attributes(game_object, attr_type, attr_name):
    assert hasattr(game_object, attr_name), (
        f'Убедитесь, что у объектов класса `GameObject` определен {attr_type} '
        f'`{attr_name}`.'
    )


EXPECTED_APPLE_ATTRS = (
    ('атрибут', 'position'),
    ('атрибут', 'body_color'),
    ('метод', 'draw'),
    ('метод', 'randomize_position'),
)


def test_apple_inherits_from_game_object(_the_snake):
    assert issubclass(_the_snake.Apple, _the_snake.GameObject), (
        'Класс `Apple` должен наследоваться от класса `GameObject`.'
    )


@pytest.mark.parametrize(
    'attr_type, attr_name',
    EXPECTED_APPLE_ATTRS,
    ids=[elem[1] for elem in EXPECTED_APPLE_ATTRS]
)
def test_apple_attributes(apple, attr_type, attr_name):
    assert hasattr(apple, attr_name), (
        f'Убедитесь, что у объектов класса `Apple` определен {attr_type} '
        f'`{attr_name}`.'
    )


EXPECTED_SNAKE_ATTRS = (
    ('атрибут', 'position'),
    ('атрибут', 'body_color'),
    ('атрибут', 'positions'),
    ('атрибут', 'direction'),
    ('метод', 'draw'),
    ('метод', 'get_head_position'),
    ('метод', 'move'),
    ('метод', 'reset'),
    ('метод', 'update_direction'),
)


def test_snake_inherits_from_game_object(_the_snake):
    assert issubclass(_the_snake.Snake, _the_snake.GameObject), (
        'Класс `Snake` должен наследоваться от класса `GameObject`.'
    )


@pytest.mark.parametrize(
    'attr_type, attr_name',
    EXPECTED_SNAKE_ATTRS,
    ids=[elem[1] for elem in EXPECTED_SNAKE_ATTRS]
)
def test_snake_attributes(snake, attr_type, attr_name):
    assert hasattr(snake, attr_name), (
        f'Убедитесь, что у объектов класса `Snake` определен {attr_type} '
        f'`{attr_name}`.'
    )


# Константы вынесены в отдельный модуль `constants`
EXPECTED_CONSTANTS = (
    'SCREEN_WIDTH',
    'SCREEN_HEIGHT',
    'GRID_SIZE',
    'GRID_WIDTH',
    'GRID_HEIGHT',
    'BOARD_BACKGROUND_COLOR',
    'UP',
    'DOWN',
    'LEFT',
    'RIGHT',
)


@pytest.mark.parametrize(
    'constant_name',
    EXPECTED_CONSTANTS,
    ids=EXPECTED_CONSTANTS
)
def test_constants_defined(constant_name):
    assert hasattr(constants, constant_name), (
        f'Убедитесь, что в модуле `constants` определена '
        f'константа `{constant_name}`.'
    )


# `screen`, `clock` и `handle_keys` теперь являются атрибутами экземпляра
# `PyGameWrapper`, а не переменными модуля `the_snake`
EXPECTED_WRAPPER_ATTRS = (
    ('атрибут', 'screen'),
    ('атрибут', 'clock'),
    ('метод', 'handle_keys'),
)


@pytest.mark.parametrize(
    'attr_type, attr_name',
    EXPECTED_WRAPPER_ATTRS,
    ids=[elem[1] for elem in EXPECTED_WRAPPER_ATTRS]
)
def test_wrapper_attributes(wrapper, attr_type, attr_name):
    assert hasattr(wrapper, attr_name), (
        f'Убедитесь, что у экземпляра класса `PyGameWrapper` '
        f'определен {attr_type} `{attr_name}`.'
    )


def test_wrapper_screen_type(wrapper):
    assert isinstance(wrapper.screen, pygame.Surface), (
        'Убедитесь, что атрибут `screen` экземпляра `PyGameWrapper` '
        f'является `{pygame.Surface.__name__}`.'
    )


def test_wrapper_clock_type(wrapper):
    assert isinstance(wrapper.clock, pygame.time.Clock), (
        'Убедитесь, что атрибут `clock` экземпляра `PyGameWrapper` '
        f'является `{pygame.time.Clock.__name__}`.'
    )


@pytest.mark.parametrize(
    'func_name',
    ('main',),
)
def test_vars_are_functions(func_name, _the_snake):
    assert callable(getattr(_the_snake, func_name, None)), (
        f'Убедитесь, что переменная `{func_name}` - это функция.'
    )
