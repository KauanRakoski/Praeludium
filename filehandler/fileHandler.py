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
            return ""
        
    def saveTextFile(self, content, path):
        """
        Saves content to .txt file of especified path. Returns true in success false for error
        """
        try:
            with open(path, 'w', encoding='utf-8') as file:
                file.write(content)
            return True
        except Exception as e:
            return False
        
    def _setupMidiFile(self, midi_messages, bpm: int):
        arquivo_mid = mido.MidiFile(type=1)
        trilha = mido.MidiTrack()
        arquivo_mid.tracks.append(trilha)
        
        tempo = mido.bpm2tempo(bpm)
        trilha.append(mido.MetaMessage('set_tempo', tempo=tempo, time=0))
                
        for msg in midi_messages:
            trilha.append(msg)
                 
        return arquivo_mid
    
    def salvarArquivoMidi(self, midi_messages, bpm: int):
        arquivo = self._setupMidiFile(midi_messages, bpm)
        
        arquivo.save("output.mid")