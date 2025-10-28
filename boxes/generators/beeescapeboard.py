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

    SIZES: dict[str, tuple[float, float]] = {
        "Zander Liebig": (520., 420.),
        "Zander Liebig Vertikale Halbzarge": (520., 210.),
        "Deutsch Normal 12er Liebig": (520., 420.),
        '10er Liebig DN Kompaktbeute': (465., 420.),
        'Dadant US 12': (509., 509.),
        'Dadant Blatt 12': (509., 509.),
        'Systembeute 10er': (509., 426.),
        'Normalmaß Beute 11er': (444., 444.),
        'Heroldbeute': (496., 440.),
        "Free": (0., 0.),
    }
    DEFAULT_SIZE = "Zander Liebig"
    COVERS = ['None', 'OutlineOnly', 'Closed', 'AirHolesRound', 'AirHolesHex', 'AirHolesSlits', 'QueenExcluder', 'DroneExcluder']
    size: str
    dx: float
    dy: float
    d: float
    D: float
    n: int
    c: float
    cover: str
    ad: float
    aD: float

    def __init__(self) -> None:
        Boxes.__init__(self)
        self.escapes: list[tuple[float, float]] = []

        ap = self.argparser
        ap.add_argument("--size", type=str, choices=self.SIZES.keys(), default=self.DEFAULT_SIZE, help="number of bee escapes")
        ap.add_argument("--dx", type=float, default=0., help="extra width (usually negative) [mm]")
        ap.add_argument("--dy", type=float, default=0., help="extra depth (usually negative) [mm]")
        ap.add_argument("--n", type=int, default=2, help="number of bee escapes")
        ap.add_argument("--d", type=float, default=112.0, help="diameter of bee escape [mm]")
        ap.add_argument("--D", type=float, default=125.0, help="diameter of bee escape cover [mm]")
        ap.add_argument("--c", type=float, default=10.0, help="thickness of inner ring [mm]")
        ap.add_argument("--cover", type=str, choices=self.COVERS, default=self.COVERS[0], help="type of cover for the bee escape holes")
        ap.add_argument("--ad", type=float, default=3.0, help="diameter of airholes [mm]")
        ap.add_argument("--aD", type=float, default=1.5, help="distance between of airholes and excluder slits [mm]")


    def render(self):
        dimensions = self.SIZES[self.size]
        self.x = dimensions[0] + self.dx
        self.y = dimensions[1] + self.dy

        self.rectangularWall(self.x, self.y, "eeee", callback=[self.render_escapes], move="right", label="Board")

        if self.cover not in ('None', 'OutlineOnly'):
            for _ in range(len(self.escapes)):
                self.parts.disc(self.D, callback=self.render_cover, move="right", label="Cover")

    def render_escapes(self) -> None:
        d = self.d
        x, y = self.x, self.y
        if d >= x or d >= y:
            raise ValueError("d to larger for board dimensions")

        n = self.n
        r = d / 2.
        R = self.D / 2.

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
            self.hole(ex, ey, r)                            # bee escape hole
            if self.cover != 'None':
                self.hole(ex, ey, R, color=Color.ETCHING)   # cover outline
            if self.cover not in ('None', 'OutlineOnly', 'Closed'):
                self.hole(ex, ey, r - self.c)  # cover inner border

    def render_cover(self):
        ex, ey = 0., 0.
        r = self.d/2
        C = r - self.c
        self.hole(ex, ey, r, color=Color.ETCHING)  # mark hole diameter
        if self.cover in ('AirHolesRound', 'AirHolesHex', 'AirHolesSlits', 'QueenExcluder', 'DroneExcluder'):
            self.hole(ex, ey, C, color=Color.ETCHING)  # cover inner border
            if self.cover in ('AirHolesRound', 'AirHolesHex'):
                self.airholes(ex, ey, C)
            elif self.cover == 'AirHolesSlits':
                self.excluder(ex, ey, C, self.ad)
            elif self.cover == 'QueenExcluder':
                self.excluder(ex, ey, C, 4.2)
            elif self.cover == 'DroneExcluder':
                self.excluder(ex, ey, C, 5.2)

    def airholes(self, ex: float, ey: float, C: float) -> None:
        if not self.ad:
            return
        hole = self.hole
        if self.cover == 'AirHolesHex':
            def hole(x, y, r):
                self.regularPolygonHole(x, y, r, n=6, a=90.)

        with self.saved_context() as ctx:
            ctx.translate(ex, ey)
            r = self.ad / 2.
            dist = self.aD + self.ad
            dx = dist
            dy = dist * math.sqrt(3) / 2.0
            C2 = C - self.aD
            CS = C2 * C2
            for nrow in range(int(C2/dy + 0.5)):
                y = nrow * dy
                l = math.sqrt(CS - y * y)
                if nrow % 2:
                    sx = dx/2.
                    mcol = int(l / dx)
                else:
                    sx = 0.
                    mcol = int(l / dx + 0.5)
                for ncol in range(mcol):
                    x = ncol * dx + sx
                    hole(x, y, r)
                    if x != 0:
                        hole(-x, y, r)
                    if y != 0:
                        hole(x, -y, r)
                        if x != 0:
                            hole(-x, -y, r)


    def excluder(self, ex: float, ey: float, C: float, d: float) -> None:
        if not self.ad:
            return

        with self.saved_context() as ctx:
            ctx.translate(ex, ey)
            D = self.aD
            D2 = D/2.
            r = d / 2.
            dist = D + d
            C2 = C - D
            CS = C2 * C2
            for nrow in range(int(C2 / dist + 0.5)):
                y = nrow * dist
                l = math.sqrt(CS - y * y) - D2
                self.rectangularHole(D2, y, l, d, r, center_y=True, center_x=False)
                self.rectangularHole(-l-D2, y, l, d, r, center_y=True, center_x=False)
                if nrow != 0:
                    self.rectangularHole(D2, -y, l, d, r, center_y=True, center_x=False)
                    self.rectangularHole(-l-D2, -y, l, d, r, center_y=True, center_x=False)

