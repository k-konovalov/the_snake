# Как собрать pygame в локальном `.venv`

Эта инструкция описывает, как установить `pygame` в виртуальное окружение `.venv`, когда для вашей версии Python нет готового wheel-пакета (например, для Python 3.14) и `pip` вынужден собирать pygame из исходников.

---

## 1. Почему нужна сборка из исходников

`pygame` распространяется в виде готовых бинарных wheel-пакетов только для определённых версий Python (обычно `cp312`, `cp313` и т.д.). Если ваша версия Python новее (например, `3.14`), готового wheel нет, и `pip` автоматически переходит к сборке из исходного кода (`pygame-2.6.1.tar.gz`).

Признак того, что нужна сборка из исходников — в логе `pip` появляется:

```
Using cached pygame-2.6.1.tar.gz (14.8 MB)
Building wheel for pygame (pyproject.toml): started
```

---

## 2. Предварительные требования (системные пакеты)

Для сборки pygame из исходников нужны компилятор и SDL2-библиотеки с заголовочными файлами. На Ubuntu/Debian установите:

```bash
sudo apt-get update
sudo apt-get install -y \
    build-essential \
    python3-dev \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libfreetype-dev \
    libportmidi-dev \
    pkg-config
```

> **Примечание про Ubuntu 26.04:** пакет `libfreetype6-dev` устарел (переходный). Актуальные заголовочные файлы FreeType предоставляет пакет `libfreetype-dev`. Если `libfreetype6-dev` показывает `Installed: (none)`, это нормально — главное, чтобы был установлен `libfreetype-dev`.

Проверить, что всё установлено, можно так:

```bash
which sdl2-config pkg-config gcc make
ls /usr/include/SDL2/SDL.h
```

---

## 3. Создание виртуального окружения

Если `.venv` ещё не создан:

```bash
python3 -m venv .venv
```

---

## 4. Установка pygame в `.venv`

```bash
.venv/bin/pip install pygame
```

Если сборка прошла успешно, в конце вы увидите примерно такое:

```
Building wheel for pygame (pyproject.toml): finished with status 'done'
Created wheel for pygame: filename=pygame-2.6.1-cp314-cp314-linux_x86_64.whl
Successfully installed pygame-2.6.1
```

---

## 5. Проверка установки

```bash
.venv/bin/python -c "import pygame; print(pygame.version.ver)"
```

Ожидаемый вывод:

```
pygame 2.6.1 (SDL 2.32.10, Python 3.14.4)
```

---

## 6. Возможные проблемы

### 6.1. Ошибка `Unable to run "sdl-config"` / `sdl2-config: not found`

Значит, не установлены SDL2-библиотеки разработчика. Установите `libsdl2-dev` (см. шаг 2) и убедитесь, что `sdl2-config` доступен в `PATH`:

```bash
which sdl2-config
```

### 6.2. Ошибка `pkg-config: not found`

Установите `pkg-config` (см. шаг 2).

### 6.3. Ошибка `No matching distribution found for pygame` (с `--only-binary`)

Это означает, что для вашей версии Python нет готового wheel. Не используйте `--only-binary=:all:` — разрешите сборку из исходников (просто `pip install pygame`).

### 6.4. Предупреждение `Your system is avx2 capable but pygame was not built with support for it`

Безвредное предупреждение о производительности. Оно не влияет на работу игры. При желании можно пересобрать с флагом:

```bash
PYGAME_DETECT_AVX2=1 .venv/bin/pip install --force-reinstall --no-cache-dir pygame
```

---

## 7. Краткая шпаргалка

```bash
# 1. Системные зависимости (один раз)
sudo apt-get install -y build-essential python3-dev libsdl2-dev \
    libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
    libfreetype-dev libportmidi-dev pkg-config

# 2. Виртуальное окружение (если ещё нет)
python3 -m venv .venv

# 3. Установка pygame
.venv/bin/pip install pygame

# 4. Проверка
.venv/bin/python -c "import pygame; print(pygame.version.ver)"
```
