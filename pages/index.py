import flet as ft
from .components.inputBar import InputBar
from .components.text import Text
from .components.verticalLayout import VerticalLayout
from .components.logo import Logo

MARGIN_FROM_TOP = 200

class Index (ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        
        self.route = "/"
        self.page = page

        inputBar = InputBar()    
        welcomeTitle = Text("Bem Vindo ao Praeludium!")
        welcomeTitle.setBold(True)
        
        hint = ft.Text(
            spans=[
                ft.TextSpan("Digite um texto para ser transformado em música, ou suba um arquivo .txt.\n Se não souber como, leia a "),
                ft.TextSpan(
                    "documentação.",
                    ft.TextStyle(color=ft.Colors.BLUE_400, decoration=ft.TextDecoration.UNDERLINE),
                    on_click=lambda _: page.go("/docs")
                ),
            ],
            text_align=ft.TextAlign.CENTER
        )
        
        logo = Logo()
        
        self.vertical_alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        textLayout = VerticalLayout()

        textLayout.add_control(logo)
        textLayout.add_control(welcomeTitle)
        textLayout.add_control(hint)
        
        # It is necessary to use a container for margin adjustment, column does not have it
        HelloContainer = ft.Container(
                        content=textLayout,
                        margin=ft.margin.only(top=200)
                    )

        self.controls = [
            HelloContainer,
            inputBar
        ]