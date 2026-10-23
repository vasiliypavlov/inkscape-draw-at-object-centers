# Draw at object centers

Inkscape 1.x extension — draw shapes at object centers and connect them with lines or diagram connectors.  
Расширение для Inkscape 1.x — фигуры в центрах объектов и соединение центров линиями или соединителями диаграмм.

**Jump to / Перейти к:** [English](#english) · [Русский](#русский)

---

## English

### Features

**Shapes at centers**
- Circle, ellipse, square, rectangle — centered on each selected object.
- Fill, stroke and opacity are inherited from the source object.

**Lines between centers**
- **Consecutive pairs** — one segment between each pair of adjacent centers.
- **Single polyline** — one polyline through all centers (option to close it).
- **Mesh (all pairs)** — segment between every pair of centers.
- **Diagram connectors** — live connectors (`inkscape:connection-*`) that auto-update when the linked objects move.

**Point ordering**
- Document order, left-to-right, right-to-left, top-to-bottom, bottom-to-top, nearest-neighbor chain, radial (by angle around centroid).

**Line color**
- Black (default).
- Inherit from the source object's stroke.
- Inherit from the source object's fill.
- The source object is the one from whose center the line starts.

**Output**
- All generated lines are `<path>` elements, immediately editable with the Node tool (N) — no conversion needed.
- Optional grouping of the whole result into a single `<g>`.

### Requirements
- Inkscape **1.0** or newer.
- Python 3 (bundled with Inkscape).

### Installation

Copy `draw_at_object_centers.inx` and `draw_at_object_centers.py` into your Inkscape extensions directory, then restart Inkscape.

| OS | Path |
|---|---|
| Linux | `~/.config/inkscape/extensions/` |
| Windows | `%APPDATA%\inkscape\extensions\` |
| macOS | `~/Library/Application Support/org.inkscape.Inkscape/config/inkscape/extensions/` |

### Usage

1. Select one or more objects (or a group).
2. Open **Extensions → Custom → Draw at object centers**.
3. Choose an action, the point ordering, the line color mode, and whether to group the result.
4. Click **Apply**.

### Notes
- **Diagram connectors** are only fully honored by Inkscape when the connected objects have stable IDs; the plugin assigns IDs automatically if missing.
- **Mesh mode** ignores point ordering (all pairs are drawn).
- **Close polyline** applies only to the *single polyline* action.
- Geometry is computed in document coordinates, so groups and transformations are handled correctly.

---

## Русский

### Возможности

**Фигуры в центрах**
- Круг, овал, квадрат, прямоугольник — по центру каждого выделенного объекта.
- Заливка, обводка и прозрачность наследуются от исходного объекта.

**Линии между центрами**
- **Соседние пары** — отрезок между каждой парой соседних центров.
- **Одна ломаная** — единая линия через все центры (можно замкнуть).
- **Сетка (все пары)** — отрезок между всеми парами центров.
- **Соединители диаграмм** — «живые» соединители (`inkscape:connection-*`), которые пересчитываются при перемещении связанных объектов.

**Сортировка точек**
- Порядок документа, слева-направо, справа-налево, сверху-вниз, снизу-вверх, «ближайший сосед», радиально (по углу вокруг центра).

**Цвет линий**
- Чёрный (по умолчанию).
- Наследовать цвет обводки исходного объекта.
- Наследовать цвет заливки исходного объекта.
- Источник цвета — объект, из центра которого линия начинается.

**Результат**
- Все линии создаются как `<path>` — сразу редактируются инструментом узлов (N), без предварительной конвертации.
- Опциональное объединение всего результата в одну группу `<g>`.

### Требования
- Inkscape **1.0** или новее.
- Python 3 (поставляется вместе с Inkscape).

### Установка

Скопируйте `draw_at_object_centers.inx` и `draw_at_object_centers.py` в папку расширений Inkscape и перезапустите программу.

| ОС | Путь |
|---|---|
| Linux | `~/.config/inkscape/extensions/` |
| Windows | `%APPDATA%\inkscape\extensions\` |
| macOS | `~/Library/Application Support/org.inkscape.Inkscape/config/inkscape/extensions/` |

### Использование

1. Выделите один или несколько объектов (или группу).
2. Откройте **Расширения → Custom → Draw at object centers**.
3. Выберите действие, порядок точек, режим цвета линий и объединение в группу.
4. Нажмите **Применить**.

### Примечания
- **Соединители диаграмм** корректно работают, когда у связанных объектов есть стабильные ID; плагин назначает их автоматически при отсутствии.
- Режим **«Сетка»** игнорирует сортировку (рисуются все пары).
- Параметр **«Замкнуть ломаную»** действует только для режима «одна ломаная».
- Геометрия считается в координатах документа, поэтому группы и трансформации учитываются корректно.

---

## License / Лицензия

**GPL-3.0-or-later**

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Эта программа распространяется на условиях GNU General Public License версии 3 или (по вашему выбору) любой более поздней версии.
