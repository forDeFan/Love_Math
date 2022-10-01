"""
Static values for centralized app flow.

Set up for:

App name,
DB file name,
Languages,
App colors,
Particular screens initial numbers/ ranges for quests.
"""

APP_NAME = "I LoVE MatH"
DB_NAME = "my.db"
APP_LANG = ["pl", "en"]
# Categories en and pl have to correspond eachother at specific index.
CATEGORIES = ["multiply", "add_substract", "percent", "roman"]
CATEGORIES_PL = ["mnożenie", "dodaw./odejm.",
                 "procenty", "l.rzymskie"]
# Colors.
BLACK = (0, 0, 0, 1)
GRAY = (128 / 255, 128 / 255, 128 / 255, 1)
RED = (255 / 255, 0, 0, 1)
PINK = (250 / 255, 232 / 255, 238 / 255, 1)
GREEN = (181 / 255, 255 / 255, 235 / 255, 1)
# Screens setup at app start - can set up ranges before app start.
ROMAN_NUMBERS_SCREEN_RANGE = (1, 1500)
MULTIPLICATION_SCREEN_RANGE = ((2, 30), (2, 9))
ADD_SUBSTRACT_SCREEN_RANGE = ((2, 200), (2, 180))
