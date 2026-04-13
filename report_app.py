import flet as ft
from datetime import datetime, timedelta
import json
import os

# Файл для хранения настроек по умолчанию
SETTINGS_FILE = "default_settings.json"

def load_settings():
    """Загрузка настроек из файла"""
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_settings(settings):
    """Сохранение настроек в файл"""
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)

# Примеры данных для списков
EMPLOYEES = ["Иванов И.И.", "Петров П.П.", "Сидоров С.С.", "Смирнов А.А."]
DEPARTMENTS = ["Отдел разработки", "Отдел тестирования", "Отдел аналитики", "Отдел поддержки"]
PROJECTS = ["Проект А", "Проект Б", "Проект В", "Проект Г"]
WORK_TYPES = ["Разработка", "Тестирование", "Аналитика", "Документирование", "Консультация"]
STATUSES = ["В работе", "Выполнено", "Выполнено частично", "Не начато", "Задержано", "Отменено"]

# Ответственные по проектам (пример)
RESPONSIBLE_BY_PROJECT = {
    "Проект А": ["Менеджер 1", "Менеджер 2"],
    "Проект Б": ["Менеджер 3", "Менеджер 4"],
    "Проект В": ["Менеджер 5", "Менеджер 6"],
    "Проект Г": ["Менеджер 7", "Менеджер 8"],
}


class ReportApp(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.settings = load_settings()
        
        # Элементы управления главной формы
        self.employee_field = None
        self.department_field = None
        self.project_field = None
        self.responsible_field = None
        self.task_field = None
        self.work_type_field = None
        self.plan_field = None
        self.fact_field = None
        self.status_field = None
        self.comment_field = None
        self.date_start_picker = None
        self.date_end_picker = None
        
        # Чекбоксы настроек над формой
        self.clear_on_create_checkbox = None
        self.next_week_plans_checkbox = None

    def build(self):
        # Создаем навигационную панель
        return ft.Column(
            controls=[
                self.create_main_page(),
            ],
            expand=True,
        )

    def create_text_field_with_autocomplete(self, label, options, initial_value=None):
        """Создает текстовое поле с автодополнением"""
        return ft.TextField(
            label=label,
            value=initial_value or "",
            suggestions=[ft.InputOptionSuggestion(key=o, value=o) for o in options],
            strict=False,
            expand=True,
        )

    def get_week_number(self):
        """Получить номер текущей недели"""
        return datetime.now().isocalendar()[1]

    def get_week_dates(self):
        """Получить даты начала и окончания текущей недели"""
        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        return start_of_week.strftime("%d.%m.%Y"), end_of_week.strftime("%d.%m.%Y")

    def update_responsible_field(self, e):
        """Обновление списка ответственных при выборе проекта"""
        project = self.project_field.value
        if project and project in RESPONSIBLE_BY_PROJECT:
            self.responsible_field.suggestions = [
                ft.InputOptionSuggestion(key=r, value=r) 
                for r in RESPONSIBLE_BY_PROJECT[project]
            ]
            # Автоматически проставляем первого ответственного
            if RESPONSIBLE_BY_PROJECT[project]:
                self.responsible_field.value = RESPONSIBLE_BY_PROJECT[project][0]
        else:
            self.responsible_field.suggestions = []
            self.responsible_field.value = ""
        self.page.update()

    def on_status_change(self, e):
        """Обработка изменения статуса - показ/скрытие комментария"""
        status = self.status_field.value
        required_statuses = ["Выполнено частично", "Не начато", "Задержано", "Отменено"]
        
        if status in required_statuses:
            self.comment_field.border_color = ft.colors.RED
            self.comment_field.helper_text = "* Обязательное поле для этого статуса"
        else:
            self.comment_field.border_color = None
            self.comment_field.helper_text = ""
        self.page.update()

    def create_main_form(self):
        """Создание главной формы отчета"""
        # Получаем настройки по умолчанию
        default_employee = self.settings.get("employee", "")
        default_department = self.settings.get("department", "")
        default_project = self.settings.get("project", "")
        default_work_type = self.settings.get("work_type", "")
        default_responsible = self.settings.get("responsible", "")
        
        # Если проект задан, получаем ответственного для него
        if default_project and default_project in RESPONSIBLE_BY_PROJECT:
            if not default_responsible and RESPONSIBLE_BY_PROJECT[default_project]:
                default_responsible = RESPONSIBLE_BY_PROJECT[default_project][0]

        # Дата начала и окончания недели
        week_start, week_end = self.get_week_dates()

        # Поля формы
        self.employee_field = self.create_text_field_with_autocomplete(
            "Сотрудник", EMPLOYEES, default_employee
        )
        self.department_field = self.create_text_field_with_autocomplete(
            "Отдел", DEPARTMENTS, default_department
        )
        
        # Неделя (автоматически)
        week_label = ft.Text(f"Неделя: {self.get_week_number()}", weight=ft.FontWeight.BOLD)
        
        # Выбор дат
        self.date_start_picker = ft.TextField(
            label="Дата начала",
            value=week_start,
            read_only=True,
            expand=True,
        )
        self.date_end_picker = ft.TextField(
            label="Дата окончания",
            value=week_end,
            read_only=True,
            expand=True,
        )
        
        date_row = ft.Row(
            controls=[
                self.date_start_picker,
                self.date_end_picker,
            ],
            spacing=20,
        )
        
        self.project_field = self.create_text_field_with_autocomplete(
            "Проект", PROJECTS, default_project
        )
        self.project_field.on_change = self.update_responsible_field
        
        self.task_field = ft.TextField(
            label="Задача",
            multiline=True,
            min_lines=3,
            max_lines=5,
            expand=True,
        )
        
        self.work_type_field = self.create_text_field_with_autocomplete(
            "Тип работы", WORK_TYPES, default_work_type
        )
        
        self.plan_field = ft.TextField(
            label="План (часы)",
            keyboard_type=ft.KeyboardType.NUMBER,
            expand=True,
        )
        
        self.fact_field = ft.TextField(
            label="Факт (часы)",
            keyboard_type=ft.KeyboardType.NUMBER,
            expand=True,
        )
        
        self.status_field = self.create_text_field_with_autocomplete(
            "Статус", STATUSES
        )
        self.status_field.on_change = self.on_status_change
        
        self.comment_field = ft.TextField(
            label="Комментарий",
            multiline=True,
            min_lines=2,
            max_lines=4,
            expand=True,
        )
        
        # Ответственный (зависит от проекта)
        initial_responsible_options = []
        if default_project and default_project in RESPONSIBLE_BY_PROJECT:
            initial_responsible_options = RESPONSIBLE_BY_PROJECT[default_project]
        
        self.responsible_field = self.create_text_field_with_autocomplete(
            "Ответственный", initial_responsible_options, default_responsible
        )

        # Чекбоксы настроек над формой
        self.clear_on_create_checkbox = ft.Checkbox(
            label="Очищать поля при создании",
            value=True,
        )
        
        self.next_week_plans_checkbox = ft.Checkbox(
            label="Добавить на следующую неделю планы",
            value=False,
        )
        
        settings_row = ft.Row(
            controls=[
                self.clear_on_create_checkbox,
                self.next_week_plans_checkbox,
            ],
            spacing=30,
        )

        # Кнопка генерации отчета
        generate_button = ft.ElevatedButton(
            text="Генерировать отчёт",
            icon=ft.icons.DESCRIPTION,
            on_click=self.generate_report,
            style=ft.ButtonStyle(
                padding=ft.padding.all(15),
            ),
        )

        # Сборка формы
        form = ft.Column(
            controls=[
                ft.Text("Форма отчёта", size=20, weight=ft.FontWeight.BOLD),
                settings_row,
                ft.Divider(),
                self.employee_field,
                self.department_field,
                week_label,
                date_row,
                self.project_field,
                self.task_field,
                self.work_type_field,
                ft.Row(
                    controls=[
                        self.plan_field,
                        self.fact_field,
                    ],
                    spacing=20,
                ),
                self.status_field,
                self.comment_field,
                self.responsible_field,
                ft.Container(height=20),
                generate_button,
            ],
            spacing=10,
            expand=True,
        )

        return form

    def generate_report(self, e):
        """Генерация отчета"""
        # Проверка обязательного комментария
        status = self.status_field.value
        required_statuses = ["Выполнено частично", "Не начато", "Задержано", "Отменено"]
        
        if status in required_statuses and not self.comment_field.value.strip():
            self.page.snack_bar = ft.SnackBar(
                ft.Text("Комментарий обязателен для выбранного статуса!"),
                bgcolor=ft.colors.RED,
            )
            self.page.snack_bar.open = True
            self.page.update()
            return
        
        # Сбор данных формы
        report_data = {
            "employee": self.employee_field.value,
            "department": self.department_field.value,
            "week": self.get_week_number(),
            "date_start": self.date_start_picker.value,
            "date_end": self.date_end_picker.value,
            "project": self.project_field.value,
            "task": self.task_field.value,
            "work_type": self.work_type_field.value,
            "plan": self.plan_field.value,
            "fact": self.fact_field.value,
            "status": self.status_field.value,
            "comment": self.comment_field.value,
            "responsible": self.responsible_field.value,
        }
        
        # Если выбрано "Добавить на следующую неделю планы"
        if self.next_week_plans_checkbox.value:
            next_week = datetime.now() + timedelta(weeks=1)
            next_week_start = next_week - timedelta(days=next_week.weekday())
            next_week_end = next_week_start + timedelta(days=6)
            
            plan_data = {
                "employee": self.employee_field.value,
                "department": self.department_field.value,
                "week": next_week.isocalendar()[1],
                "date_start": next_week_start.strftime("%d.%m.%Y"),
                "date_end": next_week_end.strftime("%d.%m.%Y"),
                "project": self.project_field.value,
                "task": self.task_field.value,
                "work_type": self.work_type_field.value,
                "plan": self.plan_field.value,
            }
            report_data["next_week_plan"] = plan_data
        
        # Отображение отчета (в реальном приложении здесь была бы отправка на сервер или сохранение)
        print("Отчет сгенерирован:")
        print(json.dumps(report_data, ensure_ascii=False, indent=2))
        
        self.page.snack_bar = ft.SnackBar(
            ft.Text("Отчёт успешно сгенерирован!"),
            bgcolor=ft.colors.GREEN,
        )
        self.page.snack_bar.open = True
        
        # Очистка полей если нужно
        if self.clear_on_create_checkbox.value:
            self.clear_form()
        
        self.page.update()

    def clear_form(self):
        """Очистка формы"""
        self.employee_field.value = ""
        self.department_field.value = ""
        self.project_field.value = ""
        self.task_field.value = ""
        self.work_type_field.value = ""
        self.plan_field.value = ""
        self.fact_field.value = ""
        self.status_field.value = ""
        self.comment_field.value = ""
        self.responsible_field.value = ""
        self.responsible_field.suggestions = []
        
        # Восстанавливаем даты на текущую неделю
        week_start, week_end = self.get_week_dates()
        self.date_start_picker.value = week_start
        self.date_end_picker.value = week_end
        
        self.page.update()

    def create_settings_dialog(self):
        """Создание диалога настроек"""
        # Загружаем текущие настройки
        default_employee = self.settings.get("employee", "")
        default_department = self.settings.get("department", "")
        default_project = self.settings.get("project", "")
        default_work_type = self.settings.get("work_type", "")
        default_responsible = self.settings.get("responsible", "")
        
        # Поля настроек
        settings_employee = self.create_text_field_with_autocomplete(
            "Сотрудник (по умолчанию)", EMPLOYEES, default_employee
        )
        settings_department = self.create_text_field_with_autocomplete(
            "Отдел (по умолчанию)", DEPARTMENTS, default_department
        )
        settings_project = self.create_text_field_with_autocomplete(
            "Проект (по умолчанию)", PROJECTS, default_project
        )
        
        # Ответственный зависит от проекта
        initial_responsible_options = []
        if default_project and default_project in RESPONSIBLE_BY_PROJECT:
            initial_responsible_options = RESPONSIBLE_BY_PROJECT[default_project]
        
        settings_responsible = self.create_text_field_with_autocomplete(
            "Ответственный (по умолчанию)", initial_responsible_options, default_responsible
        )
        
        def on_project_change(e):
            project = settings_project.value
            if project and project in RESPONSIBLE_BY_PROJECT:
                settings_responsible.suggestions = [
                    ft.InputOptionSuggestion(key=r, value=r) 
                    for r in RESPONSIBLE_BY_PROJECT[project]
                ]
            else:
                settings_responsible.suggestions = []
            self.page.update()
        
        settings_project.on_change = on_project_change
        
        settings_work_type = self.create_text_field_with_autocomplete(
            "Тип работ (по умолчанию)", WORK_TYPES, default_work_type
        )

        def save_settings_handler(e):
            """Сохранение настроек"""
            self.settings = {
                "employee": settings_employee.value,
                "department": settings_department.value,
                "project": settings_project.value,
                "work_type": settings_work_type.value,
                "responsible": settings_responsible.value,
            }
            save_settings(self.settings)
            
            self.page.snack_bar = ft.SnackBar(
                ft.Text("Настройки сохранены!"),
                bgcolor=ft.colors.GREEN,
            )
            self.page.snack_bar.open = True
            dlg.open = False
            self.page.update()

        def close_dlg(e):
            dlg.open = False
            self.page.update()

        dlg = ft.AlertDialog(
            title=ft.Text("Настройки отчёта"),
            content=ft.Column(
                controls=[
                    ft.Text("Поля по умолчанию для отчёта:", weight=ft.FontWeight.BOLD),
                    settings_employee,
                    settings_department,
                    settings_project,
                    settings_work_type,
                    settings_responsible,
                ],
                tight=True,
            ),
            actions=[
                ft.TextButton("Отмена", on_click=close_dlg),
                ft.ElevatedButton("Сохранить", on_click=save_settings_handler),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        return dlg

    def create_main_page(self):
        """Создание основной страницы с боковой панелью"""
        # Создаем диалог настроек
        settings_dlg = self.create_settings_dialog()
        
        def open_settings(e):
            self.page.dialog = settings_dlg
            settings_dlg.open = True
            self.page.update()
        
        def toggle_theme(e):
            if self.page.theme_mode == ft.ThemeMode.LIGHT:
                self.page.theme_mode = ft.ThemeMode.DARK
            else:
                self.page.theme_mode = ft.ThemeMode.LIGHT
            self.page.update()

        # Боковая панель (Rail)
        rail = ft.Rail(
            selected_index=-1,
            destinations=[
                ft.RailDestination(
                    icon=ft.icons.SETTINGS,
                    label="Настройки",
                    on_click=open_settings,
                ),
                ft.RailDestination(
                    icon=ft.icons.BRIGHTNESS_6,
                    label="Тема",
                    on_click=toggle_theme,
                ),
            ],
            width=80,
        )

        # Главная форма
        main_form = self.create_main_form()

        # Основной контент
        content = ft.Row(
            controls=[
                rail,
                ft.VerticalDivider(width=1),
                ft.Container(
                    content=main_form,
                    padding=ft.padding.all(20),
                    expand=True,
                ),
            ],
            expand=True,
        )

        return content


def main(page: ft.Page):
    page.title = "Система отчётности"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 900
    page.window.height = 700
    
    app = ReportApp(page)
    page.add(app)


if __name__ == "__main__":
    ft.app(target=main)
