import flet as ft
from .components.inputBar import InputBar
from .components.inputBar import InputBar
from .components.text import Text
from .components.verticalLayout import VerticalLayout

class Index (ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        
        self.route = "/"
        self.page = page

        inputBar = InputBar()    
        welcomeTitle = Text("Bem Vindo ao Praeludium!")
        welcomeTitle.setBold(True)
        hint = Text("Digite um texto para ser transformado em música, ou suba um arquivo .txt.\n Se não souber como, leia a documentação.", "small")
        
        
        self.vertical_alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        textLayout = VerticalLayout()

        textLayout.add_control(welcomeTitle)
        textLayout.add_control(hint)
        
        self.controls = [
            textLayout,
            inputBar
        ]