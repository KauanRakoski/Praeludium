import flet as ft
from stateManager import StateManager

class playSave(ft.Container):
    def __init__(self, page, state: StateManager, on_play_click, on_save_click, on_save_text_click):
        super().__init__()
        
        self.page = page
        self.save_dialog = ft.FilePicker(on_result=self._handle_save_dialog_result)
        self.page.overlay.append(self.save_dialog)
        
        self.on_save_click_external = on_save_click
        self.on_save_text_click = on_save_text_click

        self.state = state
        
        self.play_button = ft.ElevatedButton(
            text="Tocar música",
            icon=ft.Icons.PLAY_ARROW_ROUNDED,
            on_click=on_play_click,
            bgcolor=ft.Colors.WHITE12,
            color=ft.Colors.WHITE
        )
        
        self.save_button = ft.ElevatedButton(
            text="Salvar áudio",
            icon=ft.Icons.DOWNLOAD_ROUNDED,
            on_click=self._open_save_dialog,
            bgcolor=ft.Colors.WHITE12,
            color=ft.Colors.WHITE
        )

        self.save_text_button = ft.ElevatedButton(
            text="Salvar texto",
            icon=ft.Icons.DOWNLOAD_ROUNDED,
            on_click=self._handle_save_text,
            bgcolor=ft.Colors.WHITE12,
            color=ft.Colors.WHITE
        )
        
        controls = [
            self.play_button,
            self.save_button,
            self.save_text_button
        ]
        
        row = ft.Row(controls, alignment=ft.MainAxisAlignment.CENTER)
        self.content = row
    
    def _open_save_dialog(self, e):
        """Este método é chamado pelo botão 'Salvar' para abrir o diálogo."""
        self.save_dialog.save_file(
            dialog_title="Salvar arquivo MIDI",
            file_name="musica_gerada.mid",
            allowed_extensions=["mid"]
        )
    
    def _handle_save_dialog_result(self, e: ft.FilePickerResultEvent):
        """
        Este método é chamado pelo FilePicker DEPOIS que o usuário escolhe um local.
        """
        if e.path:
            if self.on_save_click_external:
                self.on_save_click_external(e.path)
    
    def _handle_save_text(self, e):
        path = self.state.getOpenedTextFilePath()
        content = self.state.getText()
        self.on_save_text_click(content, path)
        