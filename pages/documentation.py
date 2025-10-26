import flet as ft
from .components.inputBar import InputBar
from .components.text import Text
from .components.verticalLayout import VerticalLayout
from .components.ruleTable import RuleTable
from .components.logo import Logo

class Docs (ft.View):
    def __init__(self, page: ft.Page, state):
        super().__init__()
        
        self.route = "/docs"
        self.page = page
        self.state = state
        
        self.vertical_alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
              
        welcomeTitle = Text("Bem Vindo à documentação!")
        welcomeTitle.setBold(True)
        hint = Text("Aqui você encontra as correspondências entre o texto e as ações musicais a serem tomadas", size="small")
        logo = Logo()
        
        docsTable = RuleTable(self.state.rules)

        backButton = ft.ElevatedButton(
            "Voltar",
            icon=ft.Icons.ARROW_BACK,
            on_click=lambda e: self.page.go("/")  
        )
        
        inputBar = InputBar(page=self.page,state = self.state, on_attach_click=self.on_file_selected_handler, on_submit_click=self._submit_event_handler)    
        self.input_bar = inputBar
        self.page.overlay.append(self.input_bar.file_picker)
        
        textLayout = VerticalLayout()
        textLayout.expand = True
        textLayout.scroll = ft.ScrollMode.ADAPTIVE

        textLayout.add_control(logo)
        textLayout.add_control(welcomeTitle)
        textLayout.add_control(hint)
        textLayout.add_control(backButton)
        textLayout.add_control(docsTable)
        
        self.controls = [
            textLayout,
            inputBar
        ]
        
    def on_file_selected_handler(self, file_path):
        content = self.state.handle_file_selected(file_path)
        
        if content is not None:
            self.input_bar.set_text(content)
            
    def _submit_event_handler(self, texto):
        self.state.process_text_to_music(texto)
        self.page.go("/answers")