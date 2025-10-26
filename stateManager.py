import flet as ft

OITAVA_PADRAO = 4
VOLUME_PADRAO = 64
BPM_PADRAO = 120

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
        
        self.initial_octave = OITAVA_PADRAO
        self.initial_volume = VOLUME_PADRAO
        self.initial_bpm = BPM_PADRAO
    
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
        
    def process_text_to_music(self, texto):
        if not self.conversor_service or not self.file_service:
            print("Erro: Serviços não inicializados no StateManager")
            return
            
        music_events = self.conversor_service.converter_texto(texto, initial_octave=self.initial_octave,
            initial_volume=self.initial_volume)
        self.file_service.salvarArquivoMidi(music_events, self.initial_bpm)
        
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