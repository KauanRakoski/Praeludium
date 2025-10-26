import flet as ft

from .components.inputBar import InputBar
from .components.text import Text
from .components.verticalLayout import VerticalLayout
from .components.logo import Logo
from .components.playSave import playSave

from stateManager import StateManager

class Answers(ft.View):
    def __init__(self, page, state: StateManager):
        super().__init__()
        
        self.route = "/answers"
        self.page = page
        self.state = state
        
        self.generated_sound = state.getMidiMessages()
        self.text_inputed = state.getText()
        
        self.vertical_alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        
        welcomeTitle = Text("Suas respostas!")
        welcomeTitle.setBold(True)
        
        generated_text = Text(f"Seu texto: {self.text_inputed}", "small")
        self.generated_text = generated_text
        
        backButton = ft.ElevatedButton(
            "Voltar",
            icon=ft.Icons.ARROW_BACK,
            on_click=lambda e: self.page.go("/")  
        )
        
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
        
        soundControls = playSave(on_play_click=self.state.sound_service.play_music, 
                                 on_save_click=self.state.file_service.salvarArquivoMidi,
                                 on_save_text_click=self.state.file_service.saveTextFile, 
                                 page=page, 
                                 state = self.state,
                                 )
        
        inputBar = InputBar(page=self.page, state = self.state, on_attach_click=self.state.file_service.loadTxtFile, on_submit_click=self.submit_event)    
        self.input_bar = inputBar
        self.page.overlay.append(self.input_bar.file_picker)

        textLayout = VerticalLayout()
        logo = Logo()
        
        textLayout.add_control(logo)
        textLayout.add_control(welcomeTitle)
        textLayout.add_control(generated_text)
        textLayout.add_control(backButton)
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
        self.state.process_text_to_music(texto)
        self.generated_text.value = f"Seu texto: {texto}"
        self.page.update()