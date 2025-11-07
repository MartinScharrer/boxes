# Copyright (C) 2025 by Martin Scharrer
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from boxes import *


class CardboardBox(Boxes):
    """A foldable cardboard box"""

    description = "Cutting pattern to create a foldable box from cardboard."

    ui_group = "Box"

    def __init__(self) -> None:
        super().__init__()
        self.buildArgParser("x", "y", "h", "outside")

    def render(self):
        x, y, h = self.x, self.y, self.h
        t = self.thickness
        t2 = 2 * t
        a = max(y/3, min(y/6, 25))  # width of latch
        ah = a / 2
        b = t
        lh = h * 2/3

        if self.outside:
            self.x = x = x - t2
            self.y = y = y - t2
            self.h = h = h - t2

        xh = x/2
        yh = y/2

        xs = xh
        ys = yh

        self.ctx.translate(xh + 2*h + 3*t, yh + h)

        with self.saved_context() as ctx:
            self.set_source_color(Color.OUTER_CUT)
            xp = xs
            yp = -ys
            ctx.move_to(xp, yp)
            for dx, dy in (
                (h, 0),
                (t2, t),
                (h + t, 0),
                (0, yh - ah - t),
                (t, t),
                (0, a - t2),
                (-t, t),
                (0, yh - ah - t),
                (-h - t, 0),
                (-t2, t),
                (-h, 0),
                #
                (yh - b, 0),
                (0, h - t),
                (-yh + b + t, 0),
                (-t, t),
                #
                (t, t),
                (0, y),
                (-t, 0),
                #
                (0, lh - t2),
                (-t2, t2),
                (-x + 2 * t2, 0),
                (-t2, -t2),
                (0, -lh + t2),
                #
                (-t, 0),
                (0, -y),
                (t, -t),
                #
                (-t, -t),
                (-yh + b + t, 0),
                (0, -h + t),
                (yh - b, 0),
                #
                (-h, 0),
                (-t2, -t),
                (-h - t, 0),
                (0, -yh + ah + t),
                (-t, -t),
                (0, -a + t2),
                (t, -t),
                (0, -yh + ah + t),
                (h + t, 0),
                (t2, -t),
                (h, 0),
                #
                (-yh + b, 0),
                (0, -h + t),
                (yh - b, 0),
                (t, -t),
                #
                (xh - 4 * t, 0),
                # Opening
                (0, t2),
                (t2, t2),
                (t2, 0),
                (t2, -t2),
                (0, -t2),
                #
                (xh - 4 * t, 0),
                #
                (t, t),
                (yh - b, 0),
                (0, h - t),
                (-yh + b, 0),
            ):
                xp += dx
                yp += dy
                ctx.line_to(xp, yp)

            ctx.stroke()

        with self.saved_context() as ctx:
            self.set_source_color(Color.INNER_CUT)
            for xp, yp in ((-xh + t2, -ah), (+xh - t2 - t, -ah)):
                ctx.move_to(xp, yp)
                for dx, dy in (
                    (0, a),
                    (t, 0),
                    (0, -a),
                    (-t, 0),
                ):
                    xp += dx
                    yp += dy
                    ctx.line_to(xp, yp)
                ctx.stroke()


        with self.saved_context() as ctx:
            self.set_source_color(Color.ETCHING)
            for x0, y0, dx, dy in (
                (xh + h, -yh, 0, y),
                (xh + h + t2, -yh + t, 0, y - t2),
                #
                (-xh - h, -yh, 0, y),
                (-xh - h - t2, -yh + t, 0, y - t2),
                #
                (-xh, -yh, x, 0),
                (xh, -yh, 0, y),
                (xh, yh, -x, 0),
                (-xh, yh, 0, -y),
                #
                (-xh, yh, 0, h),
                (-xh, yh + h, x, 0),
                (xh, yh + h, 0, -h),
                #
                (-xh, yh + h + y + t, x, 0),
                #
                (-xh, -yh, 0, -h + t),
                (xh, -yh, 0, -h + t),
            ):
                ctx.move_to(x0, y0)
                ctx.line_to(x0 + dx, y0 + dy)
            ctx.stroke()
