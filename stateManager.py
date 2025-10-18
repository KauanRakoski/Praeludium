class StateManager():
    def __init__(self):
        self.text = ""
        self.midi_messages = None
        
    def getText(self):
        return self.text
    
    def setText(self, text):
        self.text = text
        
    def getMidiMessages(self):
        return self.midi_messages
    
    def setMidiMessages(self, messages):
        self.midi_messages = messages