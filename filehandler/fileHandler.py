import mido

class FileHandler():
    # self is needed for python class compatibility in inputbar -> loadTxtFile
    def loadTxtFile(self, path):
        """
        Returns content for txt file of given path. Error = -
        """
        try:
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
                return content
        except Exception as e:
            return -1
        
    def saveTextFile(self, content, path):
        """
        Saves content to .txt file of especified path. Error = -1
        """
        try:
            with open(path, 'w', encoding='utf-8') as file:
                file.write(content)
        except Exception as e:
            return -1
        
    def _setupMidiFile(self, midi_messages):
        arquivo_mid = mido.MidiFile(type=1)
        trilha = mido.MidiTrack()
        arquivo_mid.tracks.append(trilha)
        
        for msg in midi_messages:
            trilha.append(msg)
                 
        return arquivo_mid
    
    def salvarArquivoMidi(self, midi_messages):
        arquivo = self._setupMidiFile(midi_messages)
        
        arquivo.save("output.mid")