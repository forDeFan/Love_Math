"""
Static values for centralized app flow.

APP, DB and LANG set up here.
COLORS set up here.
SCREENS initial numbers/ ranges set up here.
"""

APP_NAME = "I LoVE MatH"
DB_NAME = "my.db"
APP_LANG = ["pl", "en"]
# Categories en and pl have to correspond eachother at specific index.
CATEGORIES = ["multiply", "fraction", "percent", "roman"]
CATEGORIES_PL = ["mnożenie", "ułamki", "procenty", "liczby rzymskie"]
# Colors.
BLACK = (0, 0, 0, 1)
GRAY = (128 / 255, 128 / 255, 128 / 255, 1)
RED = (255 / 255, 0, 0, 1)
PINK = (250 / 255, 232 / 255, 238 / 255, 1)
GREEN = (181 / 255, 255 / 255, 235 / 255, 1)
# Screens setup at app start - can set up ranges before app start.
ROMAN_NUMBERS_SCREEN_RANGE = (1, 1500)
MULTIPLICATION_SCREEN_RANGE = ((2, 30), (2, 9))
