# pages/components/configControls.py (NOVO ARQUIVO)

import flet as ft

class ConfigControls(ft.Row):
    """
    Component for configuring initial BPM, Volume, Octave
    """
    def __init__(
        self,
        initial_bpm: int,
        initial_volume: int,
        initial_octave: int,
        on_bpm_change,
        on_volume_change,
        on_octave_change,
    ):
        super().__init__()
        
        self.alignment = ft.MainAxisAlignment.SPACE_EVENLY
        self.vertical_alignment = ft.CrossAxisAlignment.START
        
        self.bpm_slider = ft.Slider(
            min=60,
            max=240,
            divisions=18,
            value=initial_bpm,
            label="BPM: {value}",
            on_change=lambda e: on_bpm_change(int(e.control.value))
        )
        
        self.volume_slider = ft.Slider(
            min=0,
            max=127,
            divisions=127,
            value=initial_volume,
            label="Volume: {value}",
            on_change=lambda e: on_volume_change(int(e.control.value))
        )
        
        self.octave_slider = ft.Slider(
            min=1,
            max=8,
            divisions=7,
            value=initial_octave,
            label="Oitava: {value}",
            on_change=lambda e: on_octave_change(int(e.control.value))
        )
        
        self.controls = [
            ft.Column([ft.Text("BPM"), self.bpm_slider], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Column([ft.Text("Volume"), self.volume_slider], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Column([ft.Text("Oitava"), self.octave_slider], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        ]