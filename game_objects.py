"""
Классы игровых объектов.

Определяет базовый класс GameObject и его наследников — Apple (яблоко)
и Snake (змейка). Каждый объект имеет позицию на игровом поле, цвет
и метод отрисовки.
"""

import pygame
from pygame import Surface
from constants import (
    BOARD_BACKGROUND_COLOR,
    BORDER_COLOR,
    GRID_SIZE,
    GRID_HEIGHT,
    GRID_WIDTH,
    RIGHT,
)
from random import randint


class GameObject:
    """

    Базовый класс для всех игровых объектов.

    Атрибуты:
        position: Кортеж (x, y) — позиция объекта в пикселях
            относительно левого верхнего угла игрового поля.
        body_color: Кортеж RGB — цвет отрисовки объекта.
    """

    _start_point = (GRID_HEIGHT // 2, GRID_WIDTH // 2)
    position: tuple[int, int] = _start_point
    positions: list[tuple[int, int]] = []
    body_color = pygame.Color(0, 0, 0)

    def __init__(self):
        """Инициализирует базовые атрибуты объекта.

        Args:
            position: Начальная позиция объекта (x, y) в пикселях.
            body_color: Цвет объекта в формате RGB, например (255, 0, 0).
        """
        self.position = self._start_point
        self.body_color = pygame.Color(0, 0, 0)

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
            position=self.randomize_position(),
        )

    def randomize_position(self):
        """Устанавливает случайную позицию яблока в пределах игрового поля.

        Координаты выбираются так, чтобы яблоко оказалось внутри
        сетки игрового поля, выровненной по ячейкам.
        """
        self.position = (
            randint(0, GRID_HEIGHT) * GRID_SIZE,
            randint(0, GRID_WIDTH) * GRID_SIZE,
        )

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
        last: Кортеж (x, y) — позиция последнего сегмента перед
            удалением. Используется для затирания следа.
    """

    direction = RIGHT
    next_direction = None
    length = 1
    last = None

    def __init__(self):
        super().__init__(
            body_color=pygame.Color(0, 255, 0),
            position=self._start_point,
        )
        self.last = None
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None

    def get_head_position(self):
        """Возвращает позицию головы змейки.

        Returns:
            Кортеж (x, y) координат головы — первый элемент списка positions.
        """
        return self.positions[0]

    def move(self):
        """Обновляет позицию змейки на одну ячейку.

        Вычисляет новую позицию головы на основе текущего направления,
        вставляет её в начало списка positions. Если змейка не съела
        яблоко, удаляет последний сегмент (хвост). При достижении края
        экрана змейка появляется с противоположной стороны (wrap).
        """
        self.positions.insert()
        self.positions.pop()

    def eat_apple(self, apple_position):
        """Поедание яблока."""
        pass

    def reset(self):
        """Сбрасывает змейку в начальное состояние.

        Длина возвращается к 1, позиция — в центр экрана,
        направление — вправо. Вызывается при столкновении змейки
        с самой собой.
        """
        self.direction = RIGHT
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
