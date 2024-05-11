from ..draw import Font, Sheet

charset_alphabetic = "abcdefghijklmnopqrstuvwxyz" + "abcdefghijklmnopqrstuvwxyz".upper()
charset_numeric = "0123456789"
charset_symbolic = ".,!?-+/():;%&`'*#=[]\"|_<>"

charset_alphanumeric = charset_alphabetic + charset_numeric
charset_all = " " + charset_alphabetic + charset_numeric + charset_symbolic

charset = {
    "alphabetic": charset_alphabetic,
    "numeric": charset_numeric,
    "symbolic": charset_symbolic,
    "alphanumeric": charset_alphanumeric,
    "all": charset_all
}

iconset_all = [
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
    charset_all,
    Sheet("image/font/font_small_icons.png", (usx, usy), (1, 0)),
    iconset_all,
)

fontm = Font(
    Sheet("image/font/font_regular_chars.png", (umx, umy), (1, 0)),
    charset_all,
    Sheet("image/font/font_regular_icons.png", (umx, umy), (1, 0)),
    iconset_all,
)

fontl = Font(
    Sheet("image/font/font_large_chars.png", (ulx, uly), (1, 0)),
    charset_all,
    Sheet("image/font/font_large_icons.png", (ulx, uly), (1, 0)),
    iconset_all,
)