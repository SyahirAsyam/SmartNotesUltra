from Theme.Dark import DARK_THEME
from Theme.Light import LIGHT_THEME

themes = {

    "Dark": DARK_THEME,

    "Light": LIGHT_THEME

}

current_theme = "Dark"


def apply_theme(window):

    window.setStyleSheet(

        themes[current_theme]

    )