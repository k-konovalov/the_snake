"""
Точка входа игры «Изгиб Питона».

Реэкспортирует все обязательные элементы (константы, классы, функции)
для прохождения тестов через hasattr. Основной игровой цикл
реализован в функции main().
"""

from constants import SCREEN_HEIGHT, SCREEN_WIDTH, SPEED
from game_objects import Apple, GameObject, Snake
from performance import PyGamePerformance
from pygame_wrapper import PyGameWrapper

__all__ = ['Apple', 'GameObject', 'PyGamePerformance', 'Snake']


@PyGamePerformance.measure
def tick(pygame_wrapper: PyGameWrapper, snake: Snake, apple: Apple):
    """Игровой тик"""
    # Тут опишите основную логику игры.
    pygame_wrapper.clock.tick(SPEED)
    pygame_wrapper.handle_keys(snake)
    pygame_wrapper.clear()

    snake.update_direction()
    snake.move(field_size=(SCREEN_WIDTH, SCREEN_HEIGHT))

    snake.eat_apple(apple.position, apple_func=apple.randomize_position)
    snake.eat_snake(func_clear=pygame_wrapper.clear)
    apple.draw(pygame_wrapper.screen)
    snake.draw(pygame_wrapper.screen)

    pygame_wrapper.flip()


def main():
    """Основной игровой цикл.

    Инициализирует Pygame, создаёт экземпляры Snake и Apple,
    затем в бесконечном цикле:
        1. Ограничивает частоту кадров через clock.tick(SPEED).
        2. Обрабатывает нажатия клавиш через handle_keys().
        3. Обновляет направление змейки через update_direction().
        4. Двигает змейку через move().
        5. Проверяет поедание яблока (рост + новая позиция).
        6. Проверяет столкновение с собой (reset при коллизии).
        7. Отрисовывает объекты и обновляет экран.
    """
    # Инициализация PyGame:
    pygame_wrapper = PyGameWrapper()
    pygame_wrapper.launch()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        tick(pygame_wrapper, snake, apple)


if __name__ == '__main__':
    main()
