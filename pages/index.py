import flet as ft
from .components.inputBar import InputBar
from .components.text import Text
from .components.verticalLayout import VerticalLayout
from .components.logo import Logo
from stateManager import StateManager
from .components.configControls import ConfigControls

MARGIN_FROM_TOP = 200

class Index (ft.View):
    def __init__(self, page: ft.Page, state: StateManager):
        super().__init__()
        
        self.route = "/"
        self.page = page
        self.state = state
        
        self.vertical_alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        
        inputBar = InputBar(page=self.page,state = self.state, on_attach_click=self.on_file_selected_handler, on_submit_click=self._submit_event_handler)    
        self.input_bar = inputBar
        self.page.overlay.append(self.input_bar.file_picker)
        
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
                ft.TextSpan(" Ajuste abaixo os parâmetros iniciais da música."),

            ],
            text_align=ft.TextAlign.CENTER
        )
        
        config_controls = ConfigControls(
            initial_bpm=self.state.initial_bpm,
            initial_volume=self.state.initial_volume,
            initial_octave=self.state.initial_octave,
            on_bpm_change=self.state.set_initial_bpm,
            on_volume_change=self.state.set_initial_volume,
            on_octave_change=self.state.set_initial_octave
        )
        
        logo = Logo()

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
            config_controls,
            inputBar
        ]
    
    def on_file_selected_handler(self, file_path):
        content = self.state.handle_file_selected(file_path)
        
        if content is not None:
            self.input_bar.set_text(content)
            
    def _submit_event_handler(self, texto):
        self.state.process_text_to_music(texto)
        self.page.go("/answers")