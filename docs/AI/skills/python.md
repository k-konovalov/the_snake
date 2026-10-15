---
name: python
description: >-
  Ревью кода на Python. Активируется при проверке/ревью Python-кода, поиске
  ошибок, нарушений PEP 8, улучшении аннотаций типов, async/await, обработки
  исключений, тестирования и производительности.
---

# Python Code Review Guide

> Руководство по ревью кода на Python, охватывающее аннотации типов, async/await, тестирование, обработку исключений, оптимизацию производительности и другие ключевые темы.

## Содержание

- [Аннотации типов](#аннотации-типов)
- [Асинхронное программирование](#асинхронное-программирование)
- [Обработка исключений](#обработка-исключений)
- [Частые ошибки](#частые-ошибки)
- [Лучшие практики тестирования](#лучшие-практики-тестирования)
- [Оптимизация производительности](#оптимизация-производительности)
- [Стиль кода](#стиль-кода)
- [Review Checklist](#review-checklist)

---

## Аннотации типов

### Базовые аннотации типов

```python
# ❌ Без аннотаций типов IDE не может помочь
def process_data(data, count):
    return data[:count]

# ✅ С аннотациями типов
def process_data(data: str, count: int) -> str:
    return data[:count]

# ✅ Для сложных типов используем модуль typing
from typing import Optional, Union

def find_user(user_id: int) -> Optional[User]:
    """Возвращает пользователя или None"""
    return db.get(user_id)

def handle_input(value: Union[str, int]) -> str:
    """Принимает строку или целое число"""
    return str(value)
```

### Аннотации контейнерных типов

```python
from typing import List, Dict, Set, Tuple, Sequence

# ❌ Неточный тип
def get_names(users: list) -> list:
    return [u.name for u in users]

# ✅ Точный контейнерный тип (в Python 3.9+ можно напрямую list[User])
def get_names(users: List[User]) -> List[str]:
    return [u.name for u in users]

# ✅ Для последовательностей только на чтение используем Sequence (гибче)
def process_items(items: Sequence[str]) -> int:
    return len(items)

# ✅ Тип словаря
def count_words(text: str) -> Dict[str, int]:
    words: Dict[str, int] = {}
    for word in text.split():
        words[word] = words.get(word, 0) + 1
    return words

# ✅ Кортеж (фиксированная длина и типы)
def get_point() -> Tuple[float, float]:
    return (1.0, 2.0)

# ✅ Кортеж переменной длины
def get_scores() -> Tuple[int, ...]:
    return (90, 85, 92, 88)
```

### Дженерики и TypeVar

```python
from typing import TypeVar, Generic, List, Callable

T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

# ✅ Дженерик-функция
def first(items: List[T]) -> T | None:
    return items[0] if items else None

# ✅ TypeVar с ограничением
from typing import Hashable
H = TypeVar('H', bound=Hashable)

def dedupe(items: List[H]) -> List[H]:
    return list(set(items))

# ✅ Дженерик-класс
class Cache(Generic[K, V]):
    def __init__(self) -> None:
        self._data: Dict[K, V] = {}

    def get(self, key: K) -> V | None:
        return self._data.get(key)

    def set(self, key: K, value: V) -> None:
        self._data[key] = value
```

### Callable и функции обратного вызова

```python
from typing import Callable, Awaitable

# ✅ Аннотация типа функции
Handler = Callable[[str, int], bool]

def register_handler(name: str, handler: Handler) -> None:
    handlers[name] = handler

# ✅ Асинхронный обратный вызов
AsyncHandler = Callable[[str], Awaitable[dict]]

async def fetch_with_handler(
    url: str,
    handler: AsyncHandler
) -> dict:
    return await handler(url)

# ✅ Функция, возвращающая функцию
def create_multiplier(factor: int) -> Callable[[int], int]:
    def multiplier(x: int) -> int:
        return x * factor
    return multiplier
```

### TypedDict и структурированные данные

```python
from typing import TypedDict, Required, NotRequired

# ✅ Определение структуры словаря
class UserDict(TypedDict):
    id: int
    name: str
    email: str
    age: NotRequired[int]  # Python 3.11+

def create_user(data: UserDict) -> User:
    return User(**data)

# ✅ Частично обязательные поля
class ConfigDict(TypedDict, total=False):
    debug: bool
    timeout: int
    host: Required[str]  # это поле обязательно
```

### Protocol и структурная типизация

```python
from typing import Protocol, runtime_checkable

# ✅ Определение протокола (проверка типов по «утиной типизации»)
class Readable(Protocol):
    def read(self, size: int = -1) -> bytes: ...

class Closeable(Protocol):
    def close(self) -> None: ...

# Комбинированный протокол
class ReadableCloseable(Readable, Closeable, Protocol):
    pass

def process_stream(stream: Readable) -> bytes:
    return stream.read()

# ✅ Протокол, проверяемый во время выполнения
@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> None: ...

def render(obj: object) -> None:
    if isinstance(obj, Drawable):  # проверка во время выполнения
        obj.draw()
```

---

## Асинхронное программирование

> 📖 Общие паттерны конкурентности и примеры на разных языках см. в [Руководстве по асинхронности и конкурентности](cross-cutting/async-concurrency-patterns.md)

### Основы async/await

```python
import asyncio

# ❌ Синхронный блокирующий вызов
def fetch_all_sync(urls: list[str]) -> list[str]:
    results = []
    for url in urls:
        results.append(requests.get(url).text)  # последовательное выполнение
    return results

# ✅ Асинхронный конкурентный вызов
async def fetch_url(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def fetch_all(urls: list[str]) -> list[str]:
    tasks = [fetch_url(url) for url in urls]
    return await asyncio.gather(*tasks)  # конкурентное выполнение
```

### Асинхронные контекстные менеджеры

```python
from contextlib import asynccontextmanager
from typing import AsyncIterator

# ✅ Класс асинхронного контекстного менеджера
class AsyncDatabase:
    async def __aenter__(self) -> 'AsyncDatabase':
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.disconnect()

# ✅ Использование декоратора
@asynccontextmanager
async def get_connection() -> AsyncIterator[Connection]:
    conn = await create_connection()
    try:
        yield conn
    finally:
        await conn.close()

async def query_data():
    async with get_connection() as conn:
        return await conn.fetch("SELECT * FROM users")
```

### Асинхронные итераторы

```python
from typing import AsyncIterator

# ✅ Асинхронный генератор
async def fetch_pages(url: str) -> AsyncIterator[dict]:
    page = 1
    while True:
        data = await fetch_page(url, page)
        if not data['items']:
            break
        yield data
        page += 1

# ✅ Использование асинхронной итерации
async def process_all_pages():
    async for page in fetch_pages("https://api.example.com"):
        await process_page(page)
```

### Управление задачами и отмена

```python
import asyncio

# ❌ Забыли обработать отмену
async def bad_worker():
    while True:
        await do_work()  # невозможно корректно отменить

# ✅ Корректная обработка отмены
async def good_worker():
    try:
        while True:
            await do_work()
    except asyncio.CancelledError:
        await cleanup()  # освобождение ресурсов
        raise  # повторно пробрасываем, чтобы вызывающий знал об отмене

# ✅ Управление таймаутом
async def fetch_with_timeout(url: str) -> str:
    try:
        async with asyncio.timeout(10):  # Python 3.11+
            return await fetch_url(url)
    except asyncio.TimeoutError:
        return ""

# ✅ Группа задач (Python 3.11+)
async def fetch_multiple():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(fetch_url("url1"))
        task2 = tg.create_task(fetch_url("url2"))
    # Автоматически ожидает завершения всех задач, исключения распространяются
    return task1.result(), task2.result()
```

### Смешивание синхронного и асинхронного кода

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

# ✅ Запуск синхронной функции в асинхронном коде
async def run_sync_in_async():
    loop = asyncio.get_event_loop()
    # Выполнение блокирующей операции в пуле потоков
    result = await loop.run_in_executor(
        None,  # пул потоков по умолчанию
        blocking_io_function,
        arg1, arg2
    )
    return result

# ✅ Запуск асинхронной функции в синхронном коде
def run_async_in_sync():
    return asyncio.run(async_function())

# ❌ Не используйте time.sleep в асинхронном коде
async def bad_delay():
    time.sleep(1)  # заблокирует весь цикл событий!

# ✅ Используйте asyncio.sleep
async def good_delay():
    await asyncio.sleep(1)
```

### Семафоры и ограничение скорости

```python
import asyncio

# ✅ Использование семафора для ограничения конкурентности
async def fetch_with_limit(urls: list[str], max_concurrent: int = 10):
    semaphore = asyncio.Semaphore(max_concurrent)

    async def fetch_one(url: str) -> str:
        async with semaphore:
            return await fetch_url(url)

    return await asyncio.gather(*[fetch_one(url) for url in urls])

# ✅ Использование asyncio.Queue для модели «производитель-потребитель»
async def producer_consumer():
    queue: asyncio.Queue[str] = asyncio.Queue(maxsize=100)

    async def producer():
        for item in items:
            await queue.put(item)
        await queue.put(None)  # сигнал завершения

    async def consumer():
        while True:
            item = await queue.get()
            if item is None:
                break
            await process(item)
            queue.task_done()

    await asyncio.gather(producer(), consumer())
```

---

## Обработка исключений

> 📖 Общие принципы и примеры на разных языках см. в [Руководстве по обработке ошибок](cross-cutting/error-handling-principles.md)

### Лучшие практики перехвата исключений

```python
# ❌ Слишком широкий перехват
try:
    result = risky_operation()
except:  # Перехватывает всё, даже KeyboardInterrupt!
    pass

# ❌ Перехват Exception без обработки
try:
    result = risky_operation()
except Exception:
    pass  # Проглатывает все исключения, сложно отлаживать

# ✅ Перехват конкретных исключений
try:
    result = risky_operation()
except ValueError as e:
    logger.error(f"Invalid value: {e}")
    raise
except IOError as e:
    logger.error(f"IO error: {e}")
    return default_value

# ✅ Несколько типов исключений
try:
    result = parse_and_process(data)
except (ValueError, TypeError, KeyError) as e:
    logger.error(f"Data error: {e}")
    raise DataProcessingError(str(e)) from e
```

### Цепочки исключений

```python
# ❌ Потеря информации об исходном исключении
try:
    result = external_api.call()
except APIError as e:
    raise RuntimeError("API failed")  # причина потеряна

# ✅ Использование from для сохранения цепочки исключений
try:
    result = external_api.call()
except APIError as e:
    raise RuntimeError("API failed") from e

# ✅ Явный разрыв цепочки исключений (редкий случай)
try:
    result = external_api.call()
except APIError:
    raise RuntimeError("API failed") from None
```

### Пользовательские исключения

```python
# ✅ Определение иерархии бизнес-исключений
class AppError(Exception):
    """Базовое исключение приложения"""
    pass

class ValidationError(AppError):
    """Ошибка валидации данных"""
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")

class NotFoundError(AppError):
    """Ресурс не найден"""
    def __init__(self, resource: str, id: str | int):
        self.resource = resource
        self.id = id
        super().__init__(f"{resource} with id {id} not found")

# Использование
def get_user(user_id: int) -> User:
    user = db.get(user_id)
    if not user:
        raise NotFoundError("User", user_id)
    return user
```

### Исключения в контекстных менеджерах

```python
from contextlib import contextmanager

# ✅ Корректная обработка исключений в контекстном менеджере
@contextmanager
def transaction():
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

# ✅ Использование ExceptionGroup (Python 3.11+)
def process_batch(items: list) -> None:
    errors = []
    for item in items:
        try:
            process(item)
        except Exception as e:
            errors.append(e)

    if errors:
        raise ExceptionGroup("Batch processing failed", errors)
```

---

## Частые ошибки

### Изменяемые аргументы по умолчанию

```python
# ❌ Изменяемые аргументы по умолчанию
def add_item(item, items=[]):  # Ошибка! Общие для всех вызовов
    items.append(item)
    return items

# Демонстрация проблемы
add_item(1)  # [1]
add_item(2)  # [1, 2] вместо [2]!

# ✅ Использование None в качестве значения по умолчанию
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items

# ✅ Или использование field из dataclass
from dataclasses import dataclass, field

@dataclass
class Container:
    items: list = field(default_factory=list)
```

### Изменяемые атрибуты класса

```python
# ❌ Использование изменяемых атрибутов класса
class User:
    permissions = []  # Общие для всех экземпляров!

# Демонстрация проблемы
u1 = User()
u2 = User()
u1.permissions.append("admin")
print(u2.permissions)  # ["admin"] - случайно общий!

# ✅ Инициализация в __init__
class User:
    def __init__(self):
        self.permissions = []

# ✅ Использование dataclass
@dataclass
class User:
    permissions: list = field(default_factory=list)
```

### Замыкания в циклах

```python
# ❌ Замыкание захватывает переменную цикла
funcs = []
for i in range(3):
    funcs.append(lambda: i)

print([f() for f in funcs])  # [2, 2, 2] вместо [0, 1, 2]!

# ✅ Использование аргумента по умолчанию для захвата значения
funcs = []
for i in range(3):
    funcs.append(lambda i=i: i)

print([f() for f in funcs])  # [0, 1, 2]

# ✅ Использование functools.partial
from functools import partial

funcs = [partial(lambda x: x, i) for i in range(3)]
```

### is vs ==

```python
# ❌ Использование is для сравнения значений
if x is 1000:  # может не работать!
    pass

# Python кэширует малые целые числа (от -5 до 256)
a = 256
b = 256
a is b  # True

a = 257
b = 257
a is b  # False!

# ✅ Использование == для сравнения значений
if x == 1000:
    pass

# ✅ is используется только для None и синглтонов
if x is None:
    pass

if x is True:  # строгая проверка булева значения
    pass
```

### Производительность конкатенации строк

```python
# ❌ Конкатенация строк в цикле
result = ""
for item in large_list:
    result += str(item)  # сложность O(n²)

# ✅ Использование join
result = "".join(str(item) for item in large_list)  # O(n)

# ✅ Использование StringIO для построения больших строк
from io import StringIO

buffer = StringIO()
for item in large_list:
    buffer.write(str(item))
result = buffer.getvalue()
```

---

## Лучшие практики тестирования

### Основы pytest

```python
import pytest

# ✅ Понятные имена тестов
def test_user_creation_with_valid_email():
    user = User(email="test@example.com")
    assert user.email == "test@example.com"

def test_user_creation_with_invalid_email_raises_error():
    with pytest.raises(ValidationError):
        User(email="invalid")

# ✅ Параметризованные тесты
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("World", "WORLD"),
    ("", ""),
    ("123", "123"),
])
def test_uppercase(input: str, expected: str):
    assert input.upper() == expected

# ✅ Тестирование исключений
def test_division_by_zero():
    with pytest.raises(ZeroDivisionError) as exc_info:
        1 / 0
    assert "division by zero" in str(exc_info.value)
```

### Fixtures

```python
import pytest
from typing import Generator

# ✅ Базовый fixture
@pytest.fixture
def user() -> User:
    return User(name="Test User", email="test@example.com")

def test_user_name(user: User):
    assert user.name == "Test User"

# ✅ Fixture с очисткой
@pytest.fixture
def database() -> Generator[Database, None, None]:
    db = Database()
    db.connect()
    yield db
    db.disconnect()  # очистка после теста

# ✅ Асинхронный fixture
@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient() as client:
        yield client

# ✅ Общий fixture (conftest.py)
# conftest.py
@pytest.fixture(scope="session")
def app():
    """Экземпляр app, общий для всей тестовой сессии"""
    return create_app()

@pytest.fixture(scope="module")
def db(app):
    """Подключение к БД, общее для каждого тестового модуля"""
    return app.db
```

### Mock и Patch

```python
from unittest.mock import Mock, patch, AsyncMock

# ✅ Mock внешних зависимостей
def test_send_email():
    mock_client = Mock()
    mock_client.send.return_value = True

    service = EmailService(client=mock_client)
    result = service.send_welcome_email("user@example.com")

    assert result is True
    mock_client.send.assert_called_once_with(
        to="user@example.com",
        subject="Welcome!",
        body=ANY,
    )

# ✅ Patch функций уровня модуля
@patch("myapp.services.external_api.call")
def test_with_patched_api(mock_call):
    mock_call.return_value = {"status": "ok"}

    result = process_data()

    assert result["status"] == "ok"

# ✅ Асинхронный Mock
async def test_async_function():
    mock_fetch = AsyncMock(return_value={"data": "test"})

    with patch("myapp.client.fetch", mock_fetch):
        result = await get_data()

    assert result == {"data": "test"}
```

### Организация тестов

```python
# ✅ Группировка связанных тестов в класс
class TestUserAuthentication:
    """Тесты, связанные с аутентификацией пользователя"""

    def test_login_with_valid_credentials(self, user):
        assert authenticate(user.email, "password") is True

    def test_login_with_invalid_password(self, user):
        assert authenticate(user.email, "wrong") is False

    def test_login_locks_after_failed_attempts(self, user):
        for _ in range(5):
            authenticate(user.email, "wrong")
        assert user.is_locked is True

# ✅ Пометка тестов с помощью mark
@pytest.mark.slow
def test_large_data_processing():
    pass

@pytest.mark.integration
def test_database_connection():
    pass

# Запуск тестов с определённой меткой: pytest -m "not slow"
```

### Покрытие и качество

```python
# pytest.ini или pyproject.toml
[tool.pytest.ini_options]
addopts = "--cov=myapp --cov-report=term-missing --cov-fail-under=80"
testpaths = ["tests"]

# ✅ Тестирование граничных случаев
def test_empty_input():
    assert process([]) == []

def test_none_input():
    with pytest.raises(TypeError):
        process(None)

def test_large_input():
    large_data = list(range(100000))
    result = process(large_data)
    assert len(result) == 100000
```

---

## Оптимизация производительности

### Выбор структур данных

```python
# ❌ Поиск в списке O(n)
if item in large_list:  # медленно
    pass

# ✅ Поиск в множестве O(1)
large_set = set(large_list)
if item in large_set:  # быстро
    pass

# ✅ Использование модуля collections
from collections import Counter, defaultdict, deque

# Подсчёт
word_counts = Counter(words)
most_common = word_counts.most_common(10)

# Словарь со значением по умолчанию
graph = defaultdict(list)
graph[node].append(neighbor)

# Двусторонняя очередь (операции с обоих концов O(1))
queue = deque()
queue.appendleft(item)  # O(1) против list.insert(0, item) O(n)
```

### Генераторы и итераторы

```python
# ❌ Загрузка всех данных сразу
def get_all_users():
    return [User(row) for row in db.fetch_all()]  # большое потребление памяти

# ✅ Использование генератора
def get_all_users():
    for row in db.fetch_all():
        yield User(row)  # ленивая загрузка

# ✅ Генераторное выражение
sum_of_squares = sum(x**2 for x in range(1000000))  # не создаёт список

# ✅ Модуль itertools
from itertools import islice, chain, groupby

# Взять только первые 10
first_10 = list(islice(infinite_generator(), 10))

# Соединить несколько итераторов
all_items = chain(list1, list2, list3)

# Группировка
for key, group in groupby(sorted(items, key=get_key), key=get_key):
    process_group(key, list(group))
```

### Кэширование

```python
from functools import lru_cache, cache

# ✅ LRU-кэш
@lru_cache(maxsize=128)
def expensive_computation(n: int) -> int:
    return sum(i**2 for i in range(n))

# ✅ Безлимитный кэш (Python 3.9+)
@cache
def fibonacci(n: int) -> int:
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# ✅ Ручное кэширование (когда нужен больший контроль)
class DataService:
    def __init__(self):
        self._cache: dict[str, Any] = {}
        self._cache_ttl: dict[str, float] = {}

    def get_data(self, key: str) -> Any:
        if key in self._cache:
            if time.time() < self._cache_ttl[key]:
                return self._cache[key]

        data = self._fetch_data(key)
        self._cache[key] = data
        self._cache_ttl[key] = time.time() + 300  # 5 минут
        return data
```

### Параллельная обработка

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# ✅ Для IO-интенсивных задач используем пул потоков
def fetch_all_urls(urls: list[str]) -> list[str]:
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(fetch_url, urls))
    return results

# ✅ Для CPU-интенсивных задач используем пул процессов
def process_large_dataset(data: list) -> list:
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(heavy_computation, data))
    return results

# ✅ Использование as_completed для получения результатов по мере готовности
from concurrent.futures import as_completed

with ThreadPoolExecutor() as executor:
    futures = {executor.submit(fetch, url): url for url in urls}
    for future in as_completed(futures):
        url = futures[future]
        try:
            result = future.result()
        except Exception as e:
            print(f"{url} failed: {e}")
```

---

## Стиль кода

### Основные положения PEP 8

```python
# ✅ Соглашения об именовании
class MyClass:  # имена классов в PascalCase
    MAX_SIZE = 100  # константы в UPPER_SNAKE_CASE

    def method_name(self):  # методы в snake_case
        local_var = 1  # переменные в snake_case

# ✅ Порядок импортов
# 1. Стандартная библиотека
import os
import sys
from typing import Optional

# 2. Сторонние библиотеки
import numpy as np
import pandas as pd

# 3. Локальные модули
from myapp import config
from myapp.utils import helper

# ✅ Ограничение длины строки (79 или 88 символов)
# Перенос длинных выражений
result = (
    long_function_name(arg1, arg2, arg3)
    + another_long_function(arg4, arg5)
)

# ✅ Правила пустых строк
class MyClass:
    """Строка документации класса"""

    def method_one(self):
        pass

    def method_two(self):  # одна пустая строка между методами
        pass


def top_level_function():  # две пустые строки между определениями верхнего уровня
    pass
```

### Строки документации

```python
# ✅ Строка документации в стиле Google
def calculate_area(width: float, height: float) -> float:
    """Вычисляет площадь прямоугольника.

    Args:
        width: Ширина прямоугольника (должна быть положительной).
        height: Высота прямоугольника (должна быть положительной).

    Returns:
        Площадь прямоугольника.

    Raises:
        ValueError: Если width или height отрицательны.

    Example:
        >>> calculate_area(3, 4)
        12.0
    """
    if width < 0 or height < 0:
        raise ValueError("Dimensions must be positive")
    return width * height

# ✅ Строка документации класса
class DataProcessor:
    """Класс для обработки и преобразования данных.

    Attributes:
        source: Путь к источнику данных.
        format: Формат вывода ('json' или 'csv').

    Example:
        >>> processor = DataProcessor("data.csv")
        >>> processor.process()
    """
```

### Современные возможности Python

```python
# ✅ f-строки (Python 3.6+)
name = "World"
print(f"Hello, {name}!")

# С выражениями
print(f"Result: {1 + 2 = }")  # "Result: 1 + 2 = 3"

# ✅ Оператор моржа (Python 3.8+)
if (n := len(items)) > 10:
    print(f"List has {n} items")

# ✅ Разделители позиционных аргументов (Python 3.8+)
def greet(name, /, greeting="Hello", *, punctuation="!"):
    """name передаётся только позиционно, punctuation - только по ключу"""
    return f"{greeting}, {name}{punctuation}"

# ✅ Сопоставление с образцом (Python 3.10+)
def handle_response(response: dict):
    match response:
        case {"status": "ok", "data": data}:
            return process_data(data)
        case {"status": "error", "message": msg}:
            raise APIError(msg)
        case _:
            raise ValueError("Unknown response format")
```

---

## Review Checklist

### Безопасность типов
- [ ] Функции имеют аннотации типов (параметры и возвращаемое значение)
- [ ] Используется `Optional` для явного указания возможного None
- [ ] Дженерики используются корректно
- [ ] Проверка mypy проходит (без ошибок)
- [ ] Избегается использование `Any`, при необходимости добавляется поясняющий комментарий

### Асинхронный код
- [ ] async/await используются корректно в паре
- [ ] В асинхронном коде нет блокирующих вызовов
- [ ] Корректно обрабатывается `CancelledError`
- [ ] Для конкурентного выполнения используется `asyncio.gather` или `TaskGroup`
- [ ] Ресурсы корректно освобождаются (async context manager)

### Обработка исключений
- [ ] Перехватываются конкретные типы исключений, без «голого» `except:`
- [ ] Цепочка исключений сохраняется через `from`
- [ ] Пользовательские исключения наследуются от подходящего базового класса
- [ ] Сообщения об исключениях информативны и удобны для отладки

### Структуры данных
- [ ] Нет изменяемых аргументов по умолчанию (list, dict, set)
- [ ] Атрибуты класса не являются изменяемыми объектами
- [ ] Выбрана правильная структура данных (set vs list для поиска)
- [ ] Для больших наборов данных используются генераторы, а не списки

### Тестирование
- [ ] Покрытие тестами соответствует норме (рекомендуется ≥80%)
- [ ] Имена тестов понятно описывают тестируемый сценарий
- [ ] Граничные случаи покрыты тестами
- [ ] Mock корректно изолирует внешние зависимости
- [ ] Для асинхронного кода есть соответствующие асинхронные тесты

### Стиль кода
- [ ] Соблюдается руководство по стилю PEP 8
- [ ] Функции и классы имеют docstring
- [ ] Порядок импортов корректен (стандартная библиотека, сторонние, локальные)
- [ ] Именование согласовано и осмысленно
- [ ] Используются современные возможности Python (f-string, walrus operator и т.д.)

### Производительность
- [ ] Избегается повторное создание объектов в циклах
- [ ] Для конкатенации строк используется join
- [ ] Разумно используется кэширование (@lru_cache)
- [ ] Для IO/CPU-интенсивных задач используется подходящий способ параллелизма
