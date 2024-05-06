from library.font import *
from library.sheet import *

font_chars = " abcdefghijklmnopqrstuvwxyz" +\
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ" +\
    "0123456789.,!?-+/():;%&`'*#=[]\"|_"

font_icons = [
    "", "bar_left", "bar_middle", "bar_right", "dev", "buff", "debuff",
    "gp", "xp", "hp", "mp", "weapon", "armor", "fire"
]

fonts = Font(
    Sheet("image/font/font_small_chars.png", (8, 16), (1, 0)),
    font_chars,
    Sheet("image/font/font_small_icons.png", (8, 16), (1, 0)),
    font_icons,
)

fontm = Font(
    Sheet("image/font/font_regular_chars.png", (10, 20), (1, 0)),
    font_chars,
    Sheet("image/font/font_regular_icons.png", (10, 20), (1, 0)),
    font_icons,
)

fontl = Font(
    Sheet("image/font/font_large_chars.png", (14, 28), (1, 0)),
    font_chars,
    Sheet("image/font/font_large_icons.png", (14, 28), (1, 0)),
    font_icons,
)