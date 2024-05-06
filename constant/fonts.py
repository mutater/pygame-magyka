from library.font import *
from library.sheet import *

font_chars = " abcdefghijklmnopqrstuvwxyz" +\
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ" +\
    "0123456789.,!?-+/():;%&`'*#=[]\"|_"

font_icons = [
    "", "bar_left", "bar_middle", "bar_right", "dev", "buff", "debuff",
    "gp", "xp", "hp", "mp", "weapon", "armor", "fire"
]

usx = 8
usy = 16

umx = 10
umy = 20

ulx = 14
uly = 28

fonts = Font(
    Sheet("image/font/font_small_chars.png", (usx, usy), (1, 0)),
    font_chars,
    Sheet("image/font/font_small_icons.png", (usx, usy), (1, 0)),
    font_icons,
)

fontm = Font(
    Sheet("image/font/font_regular_chars.png", (umx, umy), (1, 0)),
    font_chars,
    Sheet("image/font/font_regular_icons.png", (umx, umy), (1, 0)),
    font_icons,
)

fontl = Font(
    Sheet("image/font/font_large_chars.png", (ulx, uly), (1, 0)),
    font_chars,
    Sheet("image/font/font_large_icons.png", (ulx, uly), (1, 0)),
    font_icons,
)