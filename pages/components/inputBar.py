import flet as ft

class InputBar(ft.Row):
    def __init__(self, on_submit_click=None, on_attach_click=None):
        super().__init__()
        
        self.input_field = ft.TextField(
            hint_text="Escreva as regras aqui...",
            expand=True, 
            border_color=ft.Colors.WHITE24,
            on_submit=on_submit_click
        )
        
        self.controls = [
            ft.IconButton(
                icon=ft.Icons.ATTACH_FILE_ROUNDED,
                tooltip="Carregar arquivo .txt",
                on_click=on_attach_click
            ),
            self.input_field,
            ft.IconButton(
                icon=ft.Icons.PLAY_ARROW_ROUNDED,
                tooltip="Gerar música",
                on_click=on_submit_click
            ),
        ]