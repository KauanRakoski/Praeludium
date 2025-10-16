import flet as ft

class InputBar(ft.Row):
    """
    Input bar for handling text generation. 
    Needs to receive callbacks for 
    uploading file and submiting for conversion
    """
    def __init__(self, page, on_submit_click=None, on_attach_click=None):
        super().__init__()
        
        self.page = page
        self.on_attach_click = on_attach_click
        
        self.file_picker = ft.FilePicker(on_result=self._on_file_dialog_result)
        self.page.overlay.append(self.file_picker)
        
        self.input_field = ft.TextField(
            hint_text="Escreva as regras aqui...",
            expand=True, 
            multiline=True,
            max_lines=4,
            shift_enter=True,
            border_color=ft.Colors.WHITE24,
            on_submit=self._open_file_picker
        )
        
        self.controls = [
            ft.IconButton(
                icon=ft.Icons.ATTACH_FILE_ROUNDED,
                tooltip="Carregar arquivo .txt",
                on_click=self._open_file_picker
            ),
            self.input_field,
            ft.IconButton(
                icon=ft.Icons.PLAY_ARROW_ROUNDED,
                tooltip="Gerar música",
                on_click=on_submit_click
            ),
        ]
        
    def _open_file_picker(self, e):
        self.file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["txt"]
        )
        
    def _on_file_dialog_result(self, e):
        if e.files: # Se o usuário selecionou um arquivo
            file_path = str(e.files[0].path)
            content = self.on_attach_click(file_path)
            self._set_text(content)
        else:
            print("Seleção de arquivo cancelada.")
            
    def _set_text(self, text):
        self.input_field.value = text
        self.page.update()