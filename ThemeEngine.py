print("ThemeEngine Loaded!")

from Theme.ThemeManager import themes

import Engine.SettingEngine as setting


def load_theme(window):

    settings = setting.load_settings()

    theme_name = settings["theme"]

    window.setStyleSheet(
        themes[theme_name]
    )


def change_theme(window, theme_name):

    settings = setting.load_settings()

    settings["theme"] = theme_name

    setting.save_settings(settings)

    window.setStyleSheet(
        themes[theme_name]
    )

