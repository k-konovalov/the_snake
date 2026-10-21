# PLAN.md — План разработки игры «Изгиб Питона»

> План составлен совместно со студентом через наводящие вопросы (тьютор-сессия).
> Цель — декомпозировать задание из [`docs/main_task.md`](../main_task.md) на
> отдельные блоки логики, продумать модули, интерфейсы и базовую функциональность.

## 1. Модули и архитектура

Разбиваем код на отдельные модули. `the_snake.py` остаётся точкой входа и
**реэкспортирует** все обязательные элементы, чтобы тесты
(`tests/test_code_structure.py`) продолжали проходить через `hasattr`.

| Модуль | Содержимое |
|--------|-----------|
| `constants.py` | Все константы: размеры (`SCREEN_WIDTH`, `SCREEN_HEIGHT`), `GRID_SIZE`, `GRID_WIDTH`, `GRID_HEIGHT`, направления (`UP`, `DOWN`, `LEFT`, `RIGHT`), цвета (`BOARD_BACKGROUND_COLOR`, `BORDER_COLOR`, `APPLE_COLOR`, `SNAKE_COLOR`), `SPEED` |
| `pygame.py` | Настройки окна/заголовка. Методы/функции отрисовки объектов на игровой поверхности. **Инициализация pygame — в `main()`**, не глобально при импорте (требование GIGACODE.md) |
| `game_objects.py` | Классы `GameObject`, `Apple`, `Snake` |
| `performance.py` | Performance-декоратор для трекинга времени выполнения тика |
| `the_snake.py` | Основная логика и игровой цикл; импортирует и реэкспортирует всё нужное |

## 2. Интерфейсы классов

- **`GameObject`** (базовый): атрибуты `position`, `body_color`; метод `draw`.
- **`Apple`** (наследует `GameObject`): атрибуты `position`, `body_color`;
  методы `draw`, `randomize_position` (случайные координаты в пределах поля).
- **`Snake`** (наследует `GameObject`): атрибуты `position`, `body_color`,
  `positions`, `direction`, `next_direction`, `length`, `last`;
  методы `draw`, `get_head_position`, `move`, `reset`, `update_direction`.

Конструкторы классов не требуют аргументов кроме `self` (тесты создают объекты
без параметров).

## 3. Игровой цикл (в `main()`)

1. Инициализация pygame и настройка окна.
2. Создание экземпляров `Snake` и `Apple`.
3. Бесконечный цикл:
   - `clock.tick(SPEED)` — ограничение частоты кадров.
   - `handle_keys()` — обработка нажатий клавиш.
   - `update_direction()` — применение нового направления.
   - `move()` — движение змейки (новая голова, удаление хвоста, wrap через границы).
   - Проверка поедания яблока (увеличение длины + новая позиция яблока).
   - Проверка столкновения с собой (`reset()`).
   - Отрисовка объектов и обновление экрана.

## 4. Performance-декоратор

- Модуль `performance.py`.
- Логирует время выполнения каждого тика.
- Трекает «большой тик» — синхронизацию с частотой экрана (например, 60 FPS).
- Применяется к шагу игрового цикла / `clock.tick()`.

## 5. Docstring и PEP 8

- Всё, к чему можно написать docstring, должно содержать docstring
  (классы, методы, функции, модули).
- Код соответствует PEP 8 (flake8: max line length 79, complexity ≤ 10).

## 6. Unit-тесты

Покрыть unit-тестами всю бизнес-логику (в `tests/`):

- `Snake.move` — движение, wrap через границы, рост при поедании яблока.
- `Snake.reset` — возврат в начальное состояние.
- `Snake.get_head_position` — возврат позиции головы.
- `Snake.update_direction` — смена направления, запрет разворота на 180°.
- `Apple.randomize_position` — координаты в пределах поля.
- Столкновение змейки с собой.

## 7. Проверка в конце

- `pytest` — все тесты проходят.
- `flake8 the_snake.py` — линт без ошибок.
- Игра запускается и работает согласно правилам.

## 8. Взрослое ревью и план исправлений (2026-10-21)

### 8.1. Что проверено и работает

- `flake8` по всем модулям — чисто (exit 0); `pytest` — 35/35 green.
- Wrap по всем 4 сторонам: (0,0)+LEFT→(620,0), (620,y)+RIGHT→(0,y) и т.д.
- Столкновение с телом: `reset()` + `func_clear()` срабатывают, направление
  после reset — случайное.
- Рост при поедании: `positions` сохраняется, `length` синхронизирован.
- Защита от разворота на 180° работает на уровне ввода (`handle_keys`).

### 8.2. Найденные проблемы

**A. Корректность**

1. **Изменяемый классовый атрибут `positions`** (`game_objects.py:36`).
   Проверено: `Apple().positions is GameObject.positions` → `True` — один
   общий список на все экземпляры `GameObject`/`Apple`. У `Snake` это
   маскируется переопределением в `__init__`, но сам паттерн — классическая
   ловушка «mutable class attribute».
2. **Яблоко может spawn'иться на теле змейки** (~2 клетки из 768,
   воспроизведено в симуляции). Следующий тик — мгновенная «съеденка»,
   на ощущении — баг.
3. **Устаревшие `# noqa: F841`** в `main()` (`the_snake.py:51,54,55`):
   `pygame_wrapper`, `apple`, `snake` используются в `tick(...)`.
   Проверено: без `noqa` pyflakes не ругается.
4. **`move()`**: placeholder `new_head = ...` (Ellipsis) + if/elif-цепочка по
   4 направлениям (`game_objects.py:155-163`). Задание прямо намекает на
   дельту: «(dx, dy), которые добавляются к координатам головы».
5. **Неверный docstring `update_direction`** (`game_objects.py:210-211`):
   «Предотвращает разворот на 180 градусов» — на самом деле защита живёт в
   `PyGameWrapper.handle_keys` (`pygame_wrapper.py:68-75`).
6. **`PyGamePerformance.measure`** (`performance.py`): нет `functools.wraps`
   (обёртка теряет имя/аннотации исходной функции) и `print` на каждый тик
   (при `SPEED=5` — 5 строк в секунду спам в консоли).

**B. Аннотации типов**

7. Почти все методы без аннотаций: `GameObject.__init__/draw`,
   `Apple.__init__/randomize_position/draw`, `Snake.__init__/
   get_head_position/move/eat_apple/eat_snake/reset/update_direction/draw`,
   `PyGameWrapper.__init__/launch/handle_keys/flip/clear`, `main()`,
   `tick()` (нет `-> None`), `wrapper` в `performance.py`.
8. `handle_keys(game_object)` — тип аргумента: циклический импорт
   `Snake` → использовать `Protocol` (duck typing): у объекта нужны
   `direction` и `next_direction`.
9. `mypy` не в `requirements.txt`; у pygame нет `py.typed`, поэтому при
   добавлении нужен `ignore_missing_imports` — опционально.

**C. Тесты**

10. Обещанные в п. 6 unit-тесты логики не написаны: wrap, рост,
    столкновение, reset, границы `randomize_position`, `update_direction`.
11. Мелочи в `conftest.py`: `sys.path.append` лучше `sys.path.insert(0, ...)`;
    `os.kill(pid, 9)` — кроссплатформенно корректнее
    `check_import_process.kill()`.

**D. Стиль**

12. `constants.py:9-10` — мусорные JS-комменты `# // 2`; `constants.py:28` —
    `SPEED = 5  # 20` (остаток экспериментов).
13. `main()`: `PyGameWrapper()` создаётся (внутри `set_mode`) **до**
    `launch()` (`pygame.init()`). Работает, но логичнее init первой.

### 8.3. План исправлений (по приоритету)

1. **`game_objects.py` — класс. атрибуты и `move()`:**
   - убрать `positions` из классовых атрибутов `GameObject` и `Snake`
     (остаётся только инстанс-атрибут в `Snake.__init__`);
   - `move()`: заменить if/elif на `dx, dy = self.direction` +
     `new_head = (head_x + dx * GRID_SIZE, head_y + dy * GRID_SIZE)`;
   - wrap-логика без изменений.
2. **Аннотации типов** по п. 7–8 во всех модулях (`tuple[int, int]`,
   `Callable[[], None]`, `-> None`, Protocol в `pygame_wrapper.py`).
3. **`randomize_position(occupied: set[tuple[int, int]] | None = None)`** —
   перебирает свободные клетки; в `tick()` вызывать
   `apple.randomize_position(occupied=set(snake.positions))`.
   Подпись с дефолтом `None` сохраняет совместимость с тестами
   (вызов без аргументов).
4. **Docstring:** поправить `update_direction` (защита 180° — в
   `handle_keys`) и `move` (хвост удаляется в `eat_apple`, а не в `move`).
5. **`the_snake.py`:** убрать 3 устаревших `# noqa: F841`; аннотация
   `tick() -> None` и `main() -> None`; `launch()` до `PyGameWrapper()`
   (или init в `launch` — на выбор).
6. **`performance.py`:** `functools.wraps(func)`; аннотации; опционально —
   print только при «больших» тиках (порог, напр. > 50 мс), чтобы не
   спамить консоль.
7. **`constants.py`:** почистить комменты `# // 2`, `# 20`.
8. **Unit-тесты** `tests/test_game_logic.py` (SDL dummy уже в conftest):
   - wrap по 4 сторонам;
   - `eat_apple`: рост + вызов `apple_func`;
   - `eat_snake`: столкновение → `reset` + `func_clear`;
   - `randomize_position`: координаты на сетке и в пределах поля;
   - `randomize_position(occupied=...)`: не попадает на занятые клетки;
   - `update_direction`: применение `next_direction`;
   - `reset`: длина 1, позиция в центре, направление из допустимых.
9. **Финальная проверка:** `flake8` по всем модулям + `pytest` (старые 35
   тестов + новые) + ручной запуск игры.

Рисков нет: сигнатуры конструкторов не меняются (тесты создают объекты без
параметров), обязательные атрибуты/методы на инстансах сохраняются.