"""
    mtxPython - A framework to create matrix games.
    Copyright (C) 2016  Tobias Stampfl <info@matrixgames.rocks>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation in version 3 of the License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

from enum import Enum

###############################
# Location / Direction        #
###############################

#:
UP     = 0x0
#:
RIGHT  = 0x1
#:
DOWN   = 0x2
#:
LEFT   = 0x3


class TEXTURE:

    class GROUND:
        NONE         = 0x00
        RANDOM       = 0x01
        GRAS         = 0x02
        WOOD         = 0x03
        ROCK         = 0x04
        SAND         = 0x05
        LAVA         = 0x06
        SNOW         = 0x07
        ICE          = 0x08
        EARTH        = 0x09
        METAL        = 0x0A
        MARBLE       = 0x0B
        PAVEMENT     = 0x0C
        CONCRETE     = 0x0D


    class WALL:
        RED_BRICKS   = 0x00
        WHITE_BRICKS = 0x01
