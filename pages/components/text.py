import flet as ft

class Text(ft.Text):
    def __init__(self, text_content: str, size: str = "large"):
        super().__init__()
        
        self.value = text_content
        self.text_align = ft.TextAlign.CENTER
        
        if size == "large":
            self.style = ft.TextThemeStyle.HEADLINE_LARGE
        elif size == "medium":
            self.style = ft.TextThemeStyle.HEADLINE_MEDIUM
        else: # "small" ou qualquer outro valor será o padrão
            self.style = ft.TextThemeStyle.TITLE_LARGE
            
    def set_content(self, text_content: str):
        self.value = text_content
        self.update()
        
    def setBold(self, is_bold: bool):
        if is_bold:
            self.weight = ft.FontWeight.BOLD
        else:
            self.weight = ft.FontWeight.NORMAL