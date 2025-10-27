# Copyright (C) 2025 Martin Scharrer
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

from boxes import Boxes, edges
from boxes.Color import Color
import math



class BeeEscapeBoard(Boxes):
    """Escape boards for beekeeping."""

    ui_group = "Beekeeping"

    description = """Escape boards for beekeeping.
Allows the worker bees to escape from the honey champer to the brood champer during honey harvest."""

    SIZES = {
        "Zander Liebig": (520., 420.),
        "Zander Liebig Vertikale Halbzarge": (520., 210.),
        "Free": (0., 0.),
    }
    DEFAULT_SIZE = "Zander Liebig"

    def __init__(self) -> None:
        Boxes.__init__(self)

        ap = self.argparser

        ap.add_argument("--size", type=str, choices=self.SIZES.keys(), default=self.DEFAULT_SIZE, help="number of bee escapes")
        self.buildArgParser("x", "y")

        ap.add_argument("--d", type=float, default=112.0, help="diameter of bee escape [mm]")
        ap.add_argument("--n", type=int, default=2, help="number of bee escapes")

        self.escapes = []


    def render(self):
        if self.size != "Free":
            self.x, self.y = self.SIZES[self.size]

        self.rectangularWall(self.x, self.y, "eeee", callback=[self.render_escapes])

    def render_escapes(self) -> None:
        d = self.d
        x, y = self.x, self.y
        if d >= x or d >= y:
            raise ValueError("d to larger for board dimensions")

        n = self.n
        r = d / 2.

        def escape(ex, ey):
            self.escapes.append((ex, ey))

        if n == 1:
            escape(self.x/2., self.y/2.)
        elif n == 2:
            D = math.sqrt(x*x + y*y)
            a = (D - 2 * d) / 3.
            b = a/2. + r
            dy = min(b, y/2.)
            escape(b, dy)
            escape(x - b, y - dy)
        elif n == 0:
            pass
        else:
            raise ValueError("n must be in range 0..2")

        for ex, ey in self.escapes:
            self.hole(ex, ey, r)
