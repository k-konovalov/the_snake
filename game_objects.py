"""
Классы игровых объектов.

Определяет базовый класс GameObject и его наследников — Apple (яблоко)
и Snake (змейка). Каждый объект имеет позицию на игровом поле, цвет
и метод отрисовки.
"""

import pygame
from pygame import Surface
from constants import (
    BORDER_COLOR,
    GRID_SIZE, GRID_HEIGHT, GRID_WIDTH,
    RIGHT, LEFT, UP, DOWN,
    SCREEN_HEIGHT, SCREEN_WIDTH,
)
from random import choice, randint


class GameObject:
    """

    Базовый класс для всех игровых объектов.

    Атрибуты:
        position: Кортеж (x, y) — позиция объекта в пикселях
            относительно левого верхнего угла игрового поля.
        body_color: Кортеж RGB — цвет отрисовки объекта.
    """

    _start_point = (
        SCREEN_WIDTH // 2,   # x
        SCREEN_HEIGHT // 2,  # y
    )
    position: tuple[int, int] = _start_point
    positions: list[tuple[int, int]] = [_start_point]
    body_color = pygame.Color(0, 0, 0)

    def __init__(self, body_color=body_color, position=_start_point):
        """Инициализирует базовые атрибуты объекта.

        Args:
            position: Начальная позиция объекта (x, y) в пикселях.
            body_color: Цвет объекта в формате RGB, например (255, 0, 0).
        """
        self.position = position
        self.body_color = body_color

    def draw(self, screen: Surface):
        """Абстрактный метод отрисовки объекта на экране.

        Переопределяется в дочерних классах. По умолчанию ничего не делает.

        Args:
            screen: Surface — поверхность pygame, на которой рисуется объект.
        """
        pass


class Apple(GameObject):
    """Объект «яблоко» на игровом поле.

    Наследует позицию и цвет от GameObject. При создании занимает
    случайную позицию. При съедании змейкой перемещается в новое
    случайное место.

    Атрибуты:
        body_color: Цвет яблока — красный (255, 0, 0).
        position: Текущая позиция яблока (x, y) в пикселях.
    """

    def __init__(self):
        super().__init__(
            body_color=pygame.Color(255, 0, 0),
        )
        self.position = self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайную позицию яблока в пределах игрового поля.

        Координаты выбираются так, чтобы яблоко оказалось внутри
        сетки игрового поля, выровненной по ячейкам.
        """
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,   # x
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,  # y
        )
        return self.position

    def draw(self, screen: Surface):
        """Отрисовывает яблоко на игровой поверхности.

        Рисует квадрат размером с ячейку, залитый красным цветом,
        с обводкой цвета BORDER_COLOR.

        Args:
            screen: Surface — поверхность pygame для отрисовки.
        """
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


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

    direction = RIGHT
    next_direction = None
    length = 1

    def __init__(self):
        super().__init__(
            body_color=pygame.Color(0, 255, 0),
            position=self._start_point,
        )
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.positions = [self._start_point]
        self.position = self._start_point

    def get_head_position(self):
        """Возвращает позицию головы змейки.

        Returns:
            Кортеж (x, y) координат головы — первый элемент списка positions.
        """
        return self.positions[0]

    def move(self, field_size):
        """Обновляет позицию змейки на одну ячейку.

        Вычисляет новую позицию головы на основе текущего направления,
        вставляет её в начало списка positions. Если змейка не съела
        яблоко, удаляет последний сегмент (хвост). При достижении края
        экрана змейка появляется с противоположной стороны (wrap).
        """
        head_x, head_y = self.get_head_position()
        new_head = ...
        if self.direction == RIGHT:
            new_head = (head_x + GRID_SIZE, head_y)
        elif self.direction == LEFT:
            new_head = (head_x - GRID_SIZE, head_y)
        elif self.direction == UP:
            new_head = (head_x, head_y - GRID_SIZE)
        elif self.direction == DOWN:
            new_head = (head_x, head_y + GRID_SIZE)

        field_size_width, field_size_height = field_size
        newhead_x, newhead_y = new_head
        if newhead_x + GRID_SIZE <= 0:
            new_head = (field_size_width - GRID_SIZE, newhead_y)
        elif newhead_x + GRID_SIZE > field_size_width:
            new_head = (0, newhead_y)
        if newhead_y + GRID_SIZE <= 0:
            new_head = (newhead_x, field_size_height - GRID_SIZE)
        elif newhead_y + GRID_SIZE > field_size_height:
            new_head = (newhead_x, 0)
        self.position = new_head
        self.positions.insert(0, new_head)

    def eat_apple(self, apple_position, apple_func):
        """Поедание яблока."""
        if self.position == apple_position:
            apple_func()
            self.length = len(self.positions)
        else:
            self.positions.pop()

    def eat_snake(self, func_clear):
        """Поедание самой себя"""
        for part in self.positions[1:]:
            if self.position == part:
                self.reset()
                func_clear()
                break

    def reset(self):
        """Сбрасывает змейку в начальное состояние.

        Длина возвращается к 1, позиция — в центр экрана,
        направление выбирается случайно из четырёх возможных.
        Вызывается при столкновении змейки с самой собой.
        """
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.positions = [self._start_point]
        self.position = self._start_point
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
        for position in self.positions:  # [:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


if __name__ == '__main__':
    Apple()
    Snake()
