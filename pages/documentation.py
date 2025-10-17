import flet as ft
from .components.inputBar import InputBar
from .components.text import Text
from .components.verticalLayout import VerticalLayout
from .components.ruleTable import RuleTable
from .components.logo import Logo
from conversor.defaultRules import default_rules
from filehandler.fileHandler import FileHandler
from conversor.conversor import Conversor
from conversor.defaultRules import default_rules

class Docs (ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.route = "/docs"
        self.page = page
        
        self.fileHandler = FileHandler()
        
        rules = default_rules()
        self.conversor = Conversor(rules)
        
        inputBar = InputBar(page=self.page, on_attach_click=self.fileHandler.loadTxtFile, on_submit_click=self.submit_event)    
          
        welcomeTitle = Text("Bem Vindo à documentação!")
        welcomeTitle.setBold(True)
        hint = Text("Aqui você encontra as correspondências entre o texto e as ações musicais a serem tomadas", size="small")
        logo = Logo()
        
        docsTable = RuleTable(default_rules())
        
        self.vertical_alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        textLayout = VerticalLayout()
        textLayout.expand = True
        textLayout.scroll = ft.ScrollMode.ADAPTIVE

        textLayout.add_control(logo)
        textLayout.add_control(welcomeTitle)
        textLayout.add_control(hint)
        textLayout.add_control(docsTable)
        

        self.controls = [
            textLayout,
            inputBar
        ]
        
    def submit_event(self, texto):
        music_events = self.conversor.converter_texto(texto)
        self.fileHandler.salvarArquivoMidi(music_events)