import flet as ft

class VerticalLayout(ft.Column):
    def __init__(self, spacing: int = 15,
            alignment: ft.MainAxisAlignment = ft.MainAxisAlignment.START,
            horizontal_alignment: ft.CrossAxisAlignment = ft.CrossAxisAlignment.CENTER):
        
        super().__init__()
        
        self.controls = []
        self.spacing = spacing
        self.alignment = alignment
        self.horizontal_alignment = horizontal_alignment
        
    def add_control(self, control: ft.Control):
        self.controls.append(control)