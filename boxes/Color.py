# Copyright (C) 2013-2026 Florian Festi
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

from typing import TypeAlias

ColorValue: TypeAlias = list[float]

class Color:
    """Color values"""
    BLACK   : ColorValue = [ 0.0, 0.0, 0.0 ]
    BLUE    : ColorValue = [ 0.0, 0.0, 1.0 ]
    GREEN   : ColorValue = [ 0.0, 1.0, 0.0 ]
    RED     : ColorValue = [ 1.0, 0.0, 0.0 ]
    CYAN    : ColorValue = [ 0.0, 1.0, 1.0 ]
    YELLOW  : ColorValue = [ 1.0, 1.0, 0.0 ]
    MAGENTA : ColorValue = [ 1.0, 0.0, 1.0 ]
    WHITE   : ColorValue = [ 1.0, 1.0, 1.0 ]

    # TODO: Make this configurable
    OUTER_CUT    : ColorValue = BLACK
    INNER_CUT    : ColorValue = BLUE
    ANNOTATIONS  : ColorValue = RED
    ETCHING      : ColorValue = GREEN
    ETCHING_DEEP : ColorValue = CYAN
