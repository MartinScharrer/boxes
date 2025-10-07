# Copyright (C) 2025 Martin Scharrer
#
# Based on boxes/generators/closedbox.py, Copyright (C) 2013-2014 Florian Festi
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


class BeeQueenCage(Boxes):
    """Cage box to house a bee queen"""

    ui_group = "Beekeeping"

    description = """Cage box to house a bee queen. Opening on top suitable for Nicot-queen-rearing equipments.
    Slots can be configured as queen or drone excluders or air holes. """

    def __init__(self) -> None:
        Boxes.__init__(self)
        self.addSettingsArgs(edges.FingerJointSettings)
        self.buildArgParser("outside", x=25, y=25, h=70)

        # Custom UI parameters
        ap = self.argparser
        ap.add_argument("--d",  type=float, default=17.0, help="Diameter of top hole [mm]")
        ap.add_argument("--g",  type=float, default=3.0,  help="Gap width between holes [mm]")
        ap.add_argument("--dg", type=float, default=1.5,  help="Distance between hole rows [mm]")
        ap.add_argument("--r",  type=float, default=1.0,  help="Corner radius of holes [mm]")
        ap.add_argument("--ah", type=float, default=4.0,  help="Edge distance of holes along height [mm]")
        ap.add_argument("--ax", type=float, default=4.0,  help="Edge distance of holes along x [mm]")
        ap.add_argument("--ay", type=float, default=4.0,  help="Edge distance of holes along y [mm]")

    def get_origin(self, edges):
        edges = [self.edges.get(e, e) for e in edges]
        edges += edges  # append for wrapping around
        w0 = edges[-1].spacing() + self.spacing / 2.
        h0 = edges[0].spacing() + self.spacing / 2. + self.burn
        return w0, h0

    def render_wall(self, edges, w, h, num_holes, g, dg, r, a, label, move="right", cb=None):
        k = g + dg  # pitch of holes
        w0, h0 = self.get_origin(edges)
        xch = w0 + w/2.
        l = w - 2 * a  # length of holes
        bh = (h - k * num_holes) / 2. + dg / 2.  # offset of first hole

        for n in range(0, num_holes):
            self.rectangularHole(xch, h0 + bh + n * k, l, g, r, True, False)
        if cb:
            cb(w0, h0, w, h)
        self.rectangularWall(w, h, edges, bedBolts=[None] * 4, move=move, label=label)


    def render(self):
        ox, oy, oh = x, y, h = self.x, self.y, self.h

        if self.outside:
            x = self.adjustSize(x)
            y = self.adjustSize(y)
            h = self.adjustSize(h)

        g = self.g    # Gap
        dg = self.dg  # Distance between gaps
        ah = self.ah  # edge distance of holes (h-axis)
        ax = self.ax  # edge distance of holes (x-axis)
        ay = self.ay  # edge distance of holes (y-axis)

        r = self.r  # corner radius of holes
        d = self.d  # diameter of center hole on top

        k = g + dg  # pitch of holes

        nh = int((h - 2 * ah + dg/2) / k)  # number of holes over height
        ny = int((y - 2 * ah + dg/2) / k)  # number of holes over y (for bottom)

        self.render_wall("FFFF", x, h, nh, g, dg, r, ax, "Front", "right")
        self.render_wall("FFFF", x, h, nh, g, dg, r, ax, "Back", "right")
        self.render_wall("FfFf", y, h, nh, g, dg, r, ay, "Left", "right")
        self.render_wall("FfFf", y, h, nh, g, dg, r, ay, "Right", "right")

        self.render_wall("ffff", x, y, 0, g, dg, r, ax, "Top", "up" if 2*oy <= oh else "right",
                         cb=lambda x0, h0, x, h: self.hole(x0 + x/2., h0 + h/2., d=d))
        self.render_wall("ffff", x, y, ny, g, dg, r, ax, "Bottom", "right")


class BeeQueenCageTight(BeeQueenCage):
    """Cage box to house a bee queen - with tight spacing"""

    def open(self):
        self.reference = 0.
        Boxes.open(self)
        self.spacing = 2 * self.burn
