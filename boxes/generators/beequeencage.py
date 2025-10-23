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


class BeeQueenCageSettings(edges.Settings):
    """ Settings for BeeQueenCage

    """

    absolute_params = {
        "d": 17.0,
    }


class BeeQueenCageWallSettings(edges.Settings):
    """ Settings for walls of BeeQueenCage
    """
    NAME = None
    PREFIX = None

    params = {
        "gap_width": (3.0, float, "gap width between holes (0 for no holes) [mm]"),
        "gap_separation": (1.5, float, "distance between hole rows [mm]"),
        "radius": (1.0, float, "corner radius of holes [mm]"),
        "top_margin": (4.0, float, "distance of holes on top side [mm]"),
        "bottom_margin": (22.0, float, "distance of holes on bottom side [mm]"),
        "side_margin": (4.0, float, "side distance of holes [mm]"),
    }

    @classmethod
    def parserArguments(cls, parser, prefix=None, **defaults):
        name = cls.NAME or cls.__doc__.split("\n")[0]
        if not prefix:
            prefix = cls.PREFIX or cls.__name__[:-len("Settings")]
        group = parser.add_argument_group(name)
        group.prefix = prefix

        for name, (default, t, description) in cls.params.items():
            aname = name.replace(" ", "_")
            group.add_argument(f"--{prefix}_{aname}",
                               type=t,
                               action="store", default=default,
                               choices=None,
                               help=description)


class BeeQueenCageFrontWallSettings(BeeQueenCageWallSettings):
    """ Settings for front wall of BeeQueenCage
    """


class BeeQueenCageBackWallSettings(BeeQueenCageWallSettings):
    """ Settings for back wall of BeeQueenCage
    """


class BeeQueenCageLeftWallSettings(BeeQueenCageWallSettings):
    """ Settings for left wall of BeeQueenCage
    """


class BeeQueenCageRightWallSettings(BeeQueenCageWallSettings):
    """ Settings for right wall of BeeQueenCage
    """


class BeeQueenCageBottomWallSettings(BeeQueenCageWallSettings):
    """ Settings for bottom wall of BeeQueenCage
    """


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
        ap.add_argument("--d", type=float, default=17.0, help="Diameter of top hole [mm]")

        self.addSettingsArgs(BeeQueenCageFrontWallSettings)
        self.addSettingsArgs(BeeQueenCageBackWallSettings)
        self.addSettingsArgs(BeeQueenCageLeftWallSettings)
        self.addSettingsArgs(BeeQueenCageRightWallSettings)
        self.addSettingsArgs(BeeQueenCageBottomWallSettings)

    def callback(self, w, h, label):
        if label == "Top":
            self.render_top(w, h)
        else:
            g = getattr(self, f"BeeQueenCage{label}Wall_gap_width", 0)
            dg = getattr(self, f"BeeQueenCage{label}Wall_gap_separation", 0)
            r = getattr(self, f"BeeQueenCage{label}Wall_radius", 0)
            tm = getattr(self, f"BeeQueenCage{label}Wall_top_margin", 0)
            bm = getattr(self, f"BeeQueenCage{label}Wall_bottom_margin", 0)
            sm = getattr(self, f"BeeQueenCage{label}Wall_side_margin", 0)

            k = g + dg  # pitch of holes
            num_holes = int((h - tm - bm + dg / 2) / k)  # number of holes over height
            xch = w / 2.
            l = w - 2 * sm  # length of holes
            bh = (h - k * num_holes + dg + bm - tm) / 2.  # offset of first hole

            for n in range(0, num_holes):
                self.rectangularHole(xch, bh + n * k, l, g, r, True, False)


    def render_top(self, x, h):
        self.hole(x / 2., h / 2., d=self.d)

    def render_wall(self, edges, w, h, label, move="right"):
        self.rectangularWall(w, h, edges, bedBolts=[None] * 4,
                             move=move, label=label, callback=[lambda: self.callback(w, h, label)])

    def render(self):
        ox, oy, oh = x, y, h = self.x, self.y, self.h

        if self.outside:
            x = self.adjustSize(x)
            y = self.adjustSize(y)
            h = self.adjustSize(h)

        self.render_wall("FFFF", x, h, "Front", "right")
        self.render_wall("FFFF", x, h, "Back", "right")
        self.render_wall("FfFf", y, h, "Left", "right")
        self.render_wall("FfFf", y, h, "Right", "right")

        self.render_wall("ffff", x, y, "Top", "up" if 2 * oy <= oh else "right")
        self.render_wall("ffff", x, y, "Bottom", "right")
