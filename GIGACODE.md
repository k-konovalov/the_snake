# GIGACODE.md — the_snake

## Быстрый старт

```bash
pytest                          # все тесты
pytest tests/test_code_structure.py  # структура классов
pytest tests/test_main.py       # запуск main()
flake8 the_snake.py             # линт (исключает tests/, venv/, env/)
```

## Архитектура

Один файл: `the_snake.py`. Все классы и функции — в нём.

**Обязательные элементы модуля:**

- Константы: `SCREEN_WIDTH=640`, `SCREEN_HEIGHT=480`, `GRID_SIZE=20`, `GRID_WIDTH`, `GRID_HEIGHT`, `BOARD_BACKGROUND_COLOR`, `UP`, `DOWN`, `LEFT`, `RIGHT`, `SPEED=20`
- Переменные: `screen` (pygame.Surface), `clock` (pygame.time.Clock)
- Функции: `main()`, `handle_keys()`

**Обязательные классы:**

| Класс | Наследует | Обязательные атрибуты | Обязательные методы |
|-------|-----------|----------------------|---------------------|
| `GameObject` | — | `position`, `body_color` | `draw` |
| `Apple` | `GameObject` | `position`, `body_color` | `draw`, `randomize_position` |
| `Snake` | `GameObject` | `position`, `body_color`, `positions`, `direction` | `draw`, `get_head_position`, `move`, `reset`, `update_direction` |

## Подводные камни

- `main()` **обязательно** внутри `if __name__ == '__main__':` — иначе тесты таймаутятся
- В цикле `while True` внутри `main()` должен быть `clock.tick(SPEED)`
- Конструкторы классов не должны требовать аргументов кроме `self` (тесты создают объекты без параметров)
- Тесты запускаются с `SDL_VIDEODRIVER=dummy` — не инициализируйте pygame глобально при импорте

## Конвенции

- Flake8: max line length 79, complexity ≤ 10, single quotes, `disable-noqa = true` (CI не учитывает `# noqa`)
- Плагины flake8 (зеркало CI): flake8-print (T2xx), flake8-isort (I0xx), flake8-pie (PIE), flake8-quotes (Q000), flake8-eradicate (E800) — см. requirements.txt
- Flake8 игнорирует: W503, F811, D100/D107/D203/D205/D213/D400/D401, N806/N818
- Exclude: tests/, venv/, env/, .venv/
- flake8-pie 0.16 падает на Python ≥3.12 (`ast.Str`); в venv пропатчен shim в `.venv/lib/python3.14/site-packages/flake8_pie/__init__.py` — повторить после пересоздания venv
- Тесты проверяют наличие всех элементов через `hasattr` — имена должны совпадать точно
