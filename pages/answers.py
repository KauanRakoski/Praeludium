import flet as ft
from filehandler.fileHandler import FileHandler
from soundmanager.soundManager import SoundManager
from .components.inputBar import InputBar
from .components.text import Text
from .components.verticalLayout import VerticalLayout
from .components.logo import Logo
from .components.playSave import playSave
from soundmanager.soundManager import SoundManager
from conversor.conversor import Conversor
from conversor.defaultRules import default_rules

class Answers(ft.View):
    def __init__(self, page):
        super().__init__()
        
        self.route = "/"
        self.page = page
        
        self.soundManager = SoundManager()
        
        self.fileHandler = FileHandler()
        
        soundControls = playSave(on_play_click=self.soundManager.play_music, on_save_click=self.fileHandler.salvarArquivoMidi, page=page)
        
        rules = default_rules()
        self.conversor = Conversor(rules)
        
        inputBar = InputBar(page=self.page, on_attach_click=self.fileHandler.loadTxtFile, on_submit_click=self.submit_event)    
        welcomeTitle = Text("Suas respostas!")
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
        textLayout.add_control(soundControls)
        
        # It is necessary to use a container for margin adjustment, column does not have it
        HelloContainer = ft.Container(
                        content=textLayout,
                        margin=ft.margin.only(top=200)
                    )

        self.controls = [
            HelloContainer,
            inputBar
        ]
        
    def submit_event(self, texto):
        music_events = self.conversor.converter_texto(texto)
        self.fileHandler.salvarArquivoMidi(music_events)