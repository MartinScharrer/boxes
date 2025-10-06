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

    def render(self):
        t = self.thickness
        s = self.spacing

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

        ly = y - 2 * ay  # length of holes over y-axis
        lx = x - 2 * ax  # length of holes over x-axis

        cx = x/2 + s/2 + t  # center x
        cy = y/2 + s/2 + t  # center y

        k = g + dg  # pitch of holes

        nh = int((h - 2 * ah + dg/2) / k)  # number of holes over height
        bh = (h - k * nh)/2. + t + s/2 + self.burn + dg/2.  # y offset of first hole over height

        ny = int((y - 2 * ah + dg/2) / k)  # number of holes over y (for bottom)
        by = (y - k * ny)/2. + t + s/2 + self.burn + dg/2.  # y offset of first hole over y (for bottom)

        d2 = d3 = None

        # Front and Back
        for label in ["Front", "Back"]:
            for n in range(0, nh):
                self.rectangularHole(cx, bh + n * k, lx, g, r, True, False)
            self.rectangularWall(x, h, "FFFF", bedBolts=[d2] * 4, move="right", label=label)

        # Left and Right
        for label in ["Left", "Right"]:
            for n in range(0, nh):
                self.rectangularHole(cy, bh + n * k, ly, g, r, True, False)
            self.rectangularWall(y, h, "FfFf", bedBolts=[d3, d2, d3, d2], move="right", label=label)

        # Top
        self.hole(cx, cy, d=d)
        self.rectangularWall(x, y, "ffff", bedBolts=[d2, d3, d2, d3], move="up" if 2*oy <= oh else "right", label="Top")

        # Bottom
        for n in range(0, ny):
            self.rectangularHole(cx, by + n * k, lx, g, r, True, False)
        self.rectangularWall(x, y, "ffff", bedBolts=[d2, d3, d2, d3], label="Bottom")


class BeeQueenCageTight(BeeQueenCage):
    """Cage box to house a bee queen - with tight spacing"""

    def open(self):
        self.reference = 0.
        Boxes.open(self)
        self.spacing = 2 * self.burn
