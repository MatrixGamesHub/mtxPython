
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
