#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Draw at object centers — расширение Inkscape 1.x
"""

import math
import inkex
from inkex import Ellipse, Rectangle, Group, Line, Polyline, PathElement


def fmt(v):
    return "{:.6f}".format(float(v))


class DrawAtObjectCenters(inkex.EffectExtension):

    def add_arguments(self, pars):
        pars.add_argument("--shape_type", default="circle")
        pars.add_argument("--sort_order", default="document")
        pars.add_argument("--close_polyline", type=inkex.Boolean, default=False)
        pars.add_argument("--line_color_mode", default="black")
        pars.add_argument("--group_result", type=inkex.Boolean, default=False)

    # ------------------------------------------------------------------
    def _collect_objects(self, node):
        result = []
        if isinstance(node, Group):
            for child in node:
                result.extend(self._collect_objects(child))
        else:
            result.append(node)
        return result

    def _get_inherited(self, node, prop, default):
        current = node
        while current is not None:
            if 'style' in current.attrib:
                try:
                    s = inkex.Style(current.attrib['style'])
                    if prop in s:
                        val = s[prop]
                        if val not in (None, '', 'inherit'):
                            return val
                except Exception:
                    pass
            if prop in current.attrib:
                val = current.attrib[prop]
                if val not in (None, '', 'inherit'):
                    return val
            current = current.getparent()
        return default

    # ------------------------------------------------------------------
    # Сортировка точек
    # ------------------------------------------------------------------
    def _sort_points(self, data, sort_order):
        if sort_order in (None, '', 'document'):
            return data
        if sort_order == 'ltr':
            return sorted(data, key=lambda d: d[0])
        if sort_order == 'rtl':
            return sorted(data, key=lambda d: -d[0])
        if sort_order == 'ttb':
            return sorted(data, key=lambda d: d[1])
        if sort_order == 'btt':
            return sorted(data, key=lambda d: -d[1])
        if sort_order == 'nearest':
            return self._nearest_neighbor(data)
        if sort_order == 'radial':
            return self._radial_sort(data)
        return data

    def _nearest_neighbor(self, data):
        """Жадный алгоритм: каждый шаг — ближайшая необработанная точка."""
        if len(data) < 2:
            return data
        remaining = list(data)
        result = [remaining.pop(0)]
        while remaining:
            last = result[-1]
            idx = min(
                range(len(remaining)),
                key=lambda i: (remaining[i][0] - last[0]) ** 2 +
                              (remaining[i][1] - last[1]) ** 2,
            )
            result.append(remaining.pop(idx))
        return result

    def _radial_sort(self, data):
        """Сортировка по углу вокруг центра масс."""
        if len(data) < 2:
            return data
        cx = sum(d[0] for d in data) / len(data)
        cy = sum(d[1] for d in data) / len(data)
        return sorted(data, key=lambda d: math.atan2(d[1] - cy, d[0] - cx))

    # ------------------------------------------------------------------
    # Фабрики элементов
    # ------------------------------------------------------------------
    def _make_ellipse(self, cx, cy, rx, ry):
        el = Ellipse()
        el.set('cx', fmt(cx)); el.set('cy', fmt(cy))
        el.set('rx', fmt(rx)); el.set('ry', fmt(ry))
        return el

    def _make_rect(self, x, y, w, h):
        el = Rectangle()
        el.set('x', fmt(x)); el.set('y', fmt(y))
        el.set('width', fmt(w)); el.set('height', fmt(h))
        return el

    def _make_line(self, x1, y1, x2, y2):
        """Отрезок как <path> — сразу редактируется Node Tool."""
        el = PathElement()
        el.set('d', "M {},{} L {},{}".format(
            fmt(x1), fmt(y1), fmt(x2), fmt(y2)))
        return el

    def _make_polyline(self, points):
        """Ломаная как <path> — сразу редактируется Node Tool."""
        if not points:
            return None
        el = PathElement()
        parts = ["M {},{}".format(fmt(points[0][0]), fmt(points[0][1]))]
        for x, y in points[1:]:
            parts.append("L {},{}".format(fmt(x), fmt(y)))
        el.set('d', " ".join(parts))
        return el

    def _make_connector(self, obj_start, obj_end, style, color_mode):
        conn = PathElement()
        conn.set('d', '')
        conn.set(inkex.addNS('connector-type', 'inkscape'), 'polyline')
        conn.set(inkex.addNS('connector-curvature', 'inkscape'), '0')
        conn.set(inkex.addNS('connection-start', 'inkscape'),
                 '#{}'.format(obj_start.get_id()))
        conn.set(inkex.addNS('connection-end', 'inkscape'),
                 '#{}'.format(obj_end.get_id()))
        self._apply_line_style(conn, style, color_mode)
        return conn

    # ------------------------------------------------------------------
    # Стили
    # ------------------------------------------------------------------
    def _apply_style(self, elem, style):
        elem.style['fill'] = style['fill']
        elem.style['stroke'] = style['stroke']
        elem.style['stroke-width'] = str(style['stroke-width'])
        elem.style['opacity'] = str(style['opacity'])
        elem.style['fill-opacity'] = str(style['fill-opacity'])
        elem.style['stroke-opacity'] = str(style['stroke-opacity'])

    def _resolve_line_color(self, style, color_mode):
        if color_mode == 'stroke':
            color = style.get('stroke')
        elif color_mode == 'fill':
            color = style.get('fill')
        else:
            return '#000000'
        if color in (None, '', 'none', 'inherit'):
            return '#000000'
        return color

    def _apply_line_style(self, elem, style, color_mode):
        elem.style['fill'] = 'none'
        elem.style['stroke'] = self._resolve_line_color(style, color_mode)
        elem.style['stroke-width'] = str(style['stroke-width'])
        elem.style['opacity'] = str(style['opacity'])
        elem.style['stroke-opacity'] = str(style['stroke-opacity'])
        # рендеринг штриха
        elem.style['stroke-linecap'] = style.get('stroke-linecap') or 'round'
        elem.style['stroke-linejoin'] = style.get('stroke-linejoin') or 'round'
        elem.style['stroke-miterlimit'] = style.get('stroke-miterlimit') or '10'

    # ------------------------------------------------------------------
    def effect(self):
        shape_type = self.options.shape_type
        sort_order = self.options.sort_order
        close_polyline = bool(self.options.close_polyline)
        color_mode = self.options.line_color_mode
        group_result = bool(self.options.group_result)

        objects = []
        if self.svg.selection:
            for node in self.svg.selection.values():
                objects.extend(self._collect_objects(node))
        if not objects:
            return

        data = []
        for obj in objects:
            try:
                bbox = obj.bounding_box(transform=True)
            except Exception:
                continue
            if bbox is None:
                continue
            try:
                left = float(bbox.left); top = float(bbox.top)
                w = float(bbox.width); h = float(bbox.height)
            except Exception:
                continue
            if w <= 0 or h <= 0:
                continue

            style = {
                'fill': self._get_inherited(obj, 'fill', 'none'),
                'stroke': self._get_inherited(obj, 'stroke', 'none'),
                'stroke-width': self._get_inherited(obj, 'stroke-width', '1'),
                'opacity': self._get_inherited(obj, 'opacity', '1'),
                'fill-opacity': self._get_inherited(obj, 'fill-opacity', '1'),
                'stroke-opacity': self._get_inherited(obj, 'stroke-opacity', '1'),
                # новое — для аккуратных концов/стыков линий:
                'stroke-linecap': self._get_inherited(obj, 'stroke-linecap', 'round'),
                'stroke-linejoin': self._get_inherited(obj, 'stroke-linejoin', 'round'),
                'stroke-miterlimit': self._get_inherited(obj, 'stroke-miterlimit', '10'),
            }
            data.append((left + w / 2.0, top + h / 2.0,
                         w, h, left, top, style, obj))

        if not data:
            return

        # ---- применяем сортировку (для всех режимов, кроме mesh: там все пары) ----
        if shape_type != 'mesh':
            data = self._sort_points(data, sort_order)

        new_elements = []

        # ---- фигуры ----
        if shape_type in ('circle', 'oval', 'square', 'rectangle'):
            for cx, cy, w, h, left, top, style, _obj in data:
                if shape_type == 'circle':
                    r = min(w, h) / 2.0
                    elem = self._make_ellipse(cx, cy, r, r)
                elif shape_type == 'oval':
                    elem = self._make_ellipse(cx, cy, w / 2.0, h / 2.0)
                elif shape_type == 'square':
                    s = min(w, h)
                    elem = self._make_rect(cx - s / 2.0, cy - s / 2.0, s, s)
                else:
                    elem = self._make_rect(left, top, w, h)
                self._apply_style(elem, style)
                new_elements.append(elem)

        # ---- отдельные линии (соседние пары) ----
        elif shape_type == 'segments':
            if len(data) < 2:
                return
            for i in range(len(data) - 1):
                x1, y1 = data[i][0], data[i][1]
                x2, y2 = data[i + 1][0], data[i + 1][1]
                elem = self._make_line(x1, y1, x2, y2)
                self._apply_line_style(elem, data[i][6], color_mode)
                new_elements.append(elem)

        # ---- одна ломаная ----
        elif shape_type == 'polyline':
            if len(data) < 2:
                return
            points = [(d[0], d[1]) for d in data]
            if close_polyline and len(points) >= 3:
                points = points + [points[0]]
            elem = self._make_polyline(points)
            self._apply_line_style(elem, data[0][6], color_mode)
            new_elements.append(elem)

        # ---- все пары (mesh) ----
        elif shape_type == 'mesh':
            if len(data) < 2:
                return
            n = len(data)
            for i in range(n):
                for j in range(i + 1, n):
                    x1, y1 = data[i][0], data[i][1]
                    x2, y2 = data[j][0], data[j][1]
                    elem = self._make_line(x1, y1, x2, y2)
                    self._apply_line_style(elem, data[i][6], color_mode)
                    new_elements.append(elem)

        # ---- соединители диаграммы ----
        elif shape_type == 'diagram_connector':
            if len(data) < 2:
                return
            for i in range(len(data) - 1):
                try:
                    conn = self._make_connector(
                        data[i][7], data[i + 1][7], data[i][6], color_mode)
                    new_elements.append(conn)
                except Exception:
                    continue

        if not new_elements:
            return

        if group_result:
            group = Group()
            for elem in new_elements:
                group.append(elem)
            self.svg.append(group)
        else:
            for elem in new_elements:
                self.svg.append(elem)


if __name__ == '__main__':
    DrawAtObjectCenters().run()