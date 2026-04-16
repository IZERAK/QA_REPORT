import flet as ft
from db.dbController import Database


def settingsPage():

    width = 300

    db = Database()

    owners = db.getOwner()
    settings = db.getSettings()
    projects = db.getProjects()

    owner_options = [
        ft.dropdown.Option(
            key=str(owner["id"]),
            text=owner["name"],
        )
        for owner in owners
    ]

    project_options = [
        ft.dropdown.Option(
            key=str(project["id"]),
            text=project["name"],
        )
        for project in projects
    ]

    dd_owner = ft.Dropdown(
        label="Выберите пользователя",
        leading_icon=ft.icons.Icons.ACCOUNT_CIRCLE,
        options=owner_options,
        width=width,
        border_color=ft.Colors.PURPLE,
        border=2,
        menu_height=250,
        value=settings[0][str("id_owner")] if len(settings) > 0 else None,
    )

    dd_departament = ft.TextField(
        label="Укажите отдел",
        width=width,
        value=settings[0][str("department")] if len(settings) > 0 else None,
        border_color=ft.Colors.PURPLE,
        prefix_icon=ft.icons.Icons.BUSINESS_CENTER,
    )

    dd_project = ft.Dropdown(
        label="Выберите проект",
        border_color=ft.Colors.PURPLE,
        leading_icon=ft.icons.Icons.WORKSPACE_PREMIUM,
        width=width,
        options=project_options,
        menu_height=250,
        value=settings[0][str("id_project")] if len(settings) > 0 else None,
    )

    def handle_save(e):
        owner_val = dd_owner.value
        project_val = dd_project.value
        dept_val = dd_departament.value
        db.saveSettings(
            id_owner=int(owner_val), id_project=int(project_val), department=dept_val
        )

    form = ft.Container(
        alignment=ft.Alignment.CENTER,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(value="Значения по умолчанию", size=40),
                ft.Column(
                    expand=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.Alignment.CENTER,
                    width=width,
                    controls=[
                        ft.Container(content=dd_owner, padding=5),
                        ft.Container(content=dd_project, padding=5),
                        ft.Container(content=dd_departament, padding=5),
                        ft.IconButton(
                            icon=ft.icons.Icons.SAVE_SHARP,
                            align=ft.Alignment.TOP_RIGHT,
                            tooltip="Сохранить",
                            on_click=handle_save,
                        ),
                    ],
                ),
            ],
        ),
    )
    return form
