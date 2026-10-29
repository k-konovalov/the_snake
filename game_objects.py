"""
Классы игровых объектов.

Определяет базовый класс GameObject и его наследников — Apple (яблоко)
и Snake (змейка). Каждый объект имеет позицию на игровом поле, цвет
и метод отрисовки.
"""

from random import choice, randint

import pygame
from pygame import Surface

from constants import (APPLE_COLOR, BOARD_BACKGROUND_COLOR, BORDER_COLOR,
                       CENTER_POINT, DOWN, GRID_HEIGHT, GRID_SIZE, GRID_WIDTH,
                       LEFT, RIGHT, SNAKE_COLOR, UP)


class GameObject:
    """

    Базовый класс для всех игровых объектов.

    Атрибуты:
        position: Кортеж (x, y) — позиция объекта в пикселях
            относительно левого верхнего угла игрового поля.
        body_color: Кортеж RGB — цвет отрисовки объекта.
    """

    def __init__(self, body_color=BOARD_BACKGROUND_COLOR,
                 position=CENTER_POINT):
        """Инициализирует базовые атрибуты объекта.

        Args:
            position: Начальная позиция объекта (x, y) в пикселях.
            body_color: Цвет объекта в формате RGB, например (255, 0, 0).
        """
        self.position: tuple[int, int] = position
        self.positions: list[tuple[int, int]] = [position]
        self.body_color = pygame.Color(body_color)

    def draw(self, screen: Surface):
        """Абстрактный метод отрисовки объекта на экране.

        Переопределяется в дочерних классах. При вызове базовой
        реализации возбуждает исключение NotImplementedError.

        Args:
            screen: Surface — поверхность pygame, на которой рисуется объект.

        Raises:
            NotImplementedError: Если метод не переопределён в дочернем классе.
        """
        raise NotImplementedError(
            f'Не переопределен метод draw класса {self.__class__.__name__}',
        )

    def draw_rect(
        self,
        screen: Surface,
        position: tuple[int, int] | None = None,
    ):
        """Отрисовывает квадрат размером с ячейку на игровой поверхности.

        Args:
            screen: Surface — поверхность pygame для отрисовки.
            position: Необязательная позиция (x, y) квадрата. Если не
                указана, рисует в текущей позиции объекта.
        """
        if position is None:
            position = self.position
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Объект «яблоко» на игровом поле.

    Наследует позицию и цвет от GameObject. При создании занимает
    случайную позицию. При съедании змейкой перемещается в новое
    случайное место.

    Атрибуты:
        body_color: Цвет яблока — красный (255, 0, 0).
        position: Текущая позиция яблока (x, y) в пикселях.
    """

    def __init__(self, body_color=APPLE_COLOR, position=None,
                 restricted_positions=None):
        """Инициализирует яблоко.

        Args:
            body_color: Цвет яблока, по умолчанию APPLE_COLOR.
            position: Явная позиция (x, y). Если не указана — выбирается
                случайная.
            restricted_positions: Занятые ячейки, в которых яблоко не
                должно появиться. По умолчанию None (ограничений нет).
        """
        super().__init__(body_color=body_color, position=position)
        if position is None:
            self.randomize_position(
                restricted_positions=restricted_positions,
            )

    def get_random_pos(self) -> tuple[int, int]:
        """Возвращает случайную позицию (x, y), выровненную по сетке."""
        return (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,   # x
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,  # y
        )

    def randomize_position(
        self,
        restricted_positions: list[tuple[int, int]] | None = None,
    ) -> tuple[int, int]:
        """Устанавливает случайную позицию яблока в пределах игрового поля.

        Координаты выбираются так, чтобы яблоко оказалось внутри
        сетки игрового поля, выровненной по ячейкам, и не совпало
        с занятыми ячейками.

        Args:
            restricted_positions: Занятые ячейки, в которых яблоко не
                должно появиться. По умолчанию None (ограничений нет).

        Returns:
            Новая позиция яблока (x, y).
        """
        restricted_positions = restricted_positions or []
        new_pos = self.get_random_pos()
        while new_pos in restricted_positions:
            new_pos = self.get_random_pos()
        self.position = new_pos
        self.positions = [new_pos]
        return new_pos

    def draw(self, screen: Surface):
        """Отрисовывает яблоко на игровой поверхности.

        Рисует квадрат размером с ячейку, залитый красным цветом,
        с обводкой цвета BORDER_COLOR.

        Args:
            screen: Surface — поверхность pygame для отрисовки.
        """
        self.draw_rect(screen)


class Snake(GameObject):
    """Объект «змейка» на игровом поле.

    Программно змейка — это список координат сегментов тела.
    Управляет движением, отрисовкой, сбросом и сменой направления.

    Атрибуты:
        position: Позиция головы змейки (x, y).
        body_color: Цвет змейки — зелёный (0, 255, 0).
        positions: Список кортежей (x, y) — позиции всех сегментов тела.
            Первый элемент — голова змейки.
        direction: Кортеж (dx, dy) — текущее направление движения.
            По умолчанию RIGHT (1, 0).
        next_direction: Кортеж (dx, dy) — следующее направление,
            применится после обновления. По умолчанию None.
        length: int — текущая длина змейки в сегментах.
            Изначально 1.
    """

    def __init__(self, body_color=SNAKE_COLOR, position=CENTER_POINT):
        """Инициализирует змейку в начальном состоянии.

        Args:
            body_color: Цвет змейки, по умолчанию SNAKE_COLOR.
            position: Начальная позиция головы (x, y), по умолчанию
                центр игрового поля.
        """
        super().__init__(body_color=body_color, position=position)
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None

    def get_head_position(self):
        """Возвращает позицию головы змейки.

        Returns:
            Кортеж (x, y) координат головы — первый элемент списка positions.
        """
        return self.positions[0]

    def move(self, field_size):
        """Обновляет позицию змейки на одну ячейку.

        Вычисляет новую позицию головы по формуле
        coord = (head_coord + direction_coord * GRID_SIZE) % field_size
        для каждой координаты, вставляет её в начало списка positions.
        При достижении края экрана змейка появляется с противоположной
        стороны (wrap).
        """
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        field_width, field_height = field_size
        new_head = (
            (head_x + dx * GRID_SIZE) % field_width,
            (head_y + dy * GRID_SIZE) % field_height,
        )
        self.position = new_head
        self.positions.insert(0, new_head)

    def eat_snake(self, func_clear):
        """Поедание самой себя"""
        if self.position in self.positions[1:]:
            self.reset()
            func_clear()

    def reset(self):
        """Сбрасывает змейку в начальное состояние.

        Длина возвращается к 1, позиция — в центр экрана,
        направление выбирается случайно из четырёх возможных.
        Вызывается при столкновении змейки с самой собой.
        """
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.positions = [CENTER_POINT]
        self.position = CENTER_POINT
        self.length = 1

    def update_direction(self):
        """Применяет отложенное направление движения.

        Если next_direction не None, устанавливает direction = next_direction
        и сбрасывает next_direction в None.
        Предотвращает разворот на 180 градусов.
        """
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self, screen: Surface):
        """Отрисовывает змейку на игровой поверхности.

        Рисует каждый сегмент тела зелёным квадратом с обводкой.
        Затем затирает позицию последнего удалённого сегмента
        цветом фона, чтобы визуально змейка «ползла».

        Args:
            screen: Surface — поверхность pygame для отрисовки.
        """
        for position in self.positions:
            self.draw_rect(screen, position)


if __name__ == '__main__':
    Apple()
    Snake()
