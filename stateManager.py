import flet as ft
from conversor.conversor import Conversor, default_rules, MidiContext

DEFAULT_OCTAVE = 4
DEFAULT_VOLUME = 64
DEFAULT_BPM = 120

class StateManager():
    
    def __init__(self, page: ft.Page):
        
        self.page = page
        
        self.text = ""
        self.midi_messages = None
        self.opened_text_file_path = None
        
        self.conversor_service = None
        self.rules = None
        self.file_service = None
        self.sound_service = None
        
        self.initial_octave = DEFAULT_OCTAVE
        self.initial_volume = DEFAULT_VOLUME
        self.initial_bpm = DEFAULT_BPM
    
    def set_initial_octave(self, value: int):
        self.initial_octave = int(value)

    def set_initial_volume(self, value: int):
        self.initial_volume = int(value)

    def set_initial_bpm(self, value: int):
        self.initial_bpm = int(value)
   
    def getOpenedTextFilePath(self):
        return self.opened_text_file_path
    
    def setOpenedTextFilePath(self, path):
        self.opened_text_file_path = path

    def getText(self):
        return self.text
    
    def setText(self, text):
        self.text = text
        
    def getMidiMessages(self):
        return self.midi_messages
    
    def setMidiMessages(self, messages):
        self.midi_messages = messages


    def set_default_rules(self, rules):
        self.rules = rules
  
    def process_text_to_music(self, texto):
        if not self.conversor_service or not self.file_service:
            print("Erro: Serviços não inicializados no StateManager")
            return

        contexto_da_musica = MidiContext(
            initial_volume=self.initial_volume,
            initial_octave=self.initial_octave,
            initial_bpm=self.initial_bpm
        )

        music_events = self.conversor_service.convert_text(texto, contexto_da_musica)
        
        self.file_service.saveMidiFile(music_events)
        
        self.setText(texto)
        self.setMidiMessages(music_events)

        self.page.go("/answers") 
        
    def handle_file_selected(self, file_path):
        """
        Logic for text file selected
        """
        if not self.file_service:
            print("Erro: FileService não inicializado")
            return
            
        content = self.file_service.loadTxtFile(file_path)
        self.setOpenedTextFilePath(file_path)
    
        return content