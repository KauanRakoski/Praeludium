class StateManager():
    def __init__(self):
        self.text = ""
        self.midi_messages = None
        self.opened_text_file_path = None
    
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