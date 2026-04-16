import flet as ft


def changeTheme(page: ft.Page):
    if page.theme_mode == ft.ThemeMode.DARK:
        page.theme_mode = ft.ThemeMode.LIGHT
        page.floating_action_button.icon = ft.icons.Icons.LIGHT_MODE
    else:
        page.theme_mode = ft.ThemeMode.DARK
        page.floating_action_button.icon = ft.icons.Icons.DARK_MODE

    page.update()
