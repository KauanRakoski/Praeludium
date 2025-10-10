import flet as ft
LOGO_PATH = "assets/praeludium_logo.png"

class Logo(ft.Image):
    """
    Generates logo image, given width and height
    """
    def __init__(self, width=70, height=70):
        super().__init__()
        
        self.src = LOGO_PATH
        self.width = width
        self.height = height

    