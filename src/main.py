import flet as ft
from utility.chageTheme import changeTheme
from pages.settings import settingsPage


def main(page: ft.Page):
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.PURPLE)
    page.dark_theme = ft.Theme(color_scheme_seed=ft.Colors.DEEP_PURPLE)
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.floating_action_button = ft.FloatingActionButton(
        width=50,
        height=50,
        rotate=-25,
        icon=ft.icons.Icons.DARK_MODE,
        on_click=lambda e: changeTheme(page),
    )

    page.appbar = ft.AppBar(
        bgcolor=ft.Colors.SURFACE_CONTAINER,
        actions=[
            ft.IconButton(icon=ft.icons.Icons.SETTINGS),
        ],
    )

    page.add(settingsPage())


ft.run(main)
