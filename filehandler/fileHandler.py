import mido
import shutil

OUTPUT_FILE_NAME = "output.mid"

class FileHandler():
    # IMPORTANT: self is not directly used but is needed for python class compatibility in inputbar -> loadTxtFile.
    # Otherwise a expected one but got two arguments will be thrown
    def loadTxtFile(self, path):
        """
        Returns content for txt file of given path. Error = empty string
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
        
    def _setupMidiFile(self, midi_messages):
        arquivo_mid = mido.MidiFile(type=1)
        trilha = mido.MidiTrack()
        arquivo_mid.tracks.append(trilha)
        
        for msg in midi_messages:
            trilha.append(msg)
                 
        return arquivo_mid
    
    def salvarArquivoMidi(self, midi_messages):
        arquivo = self._setupMidiFile(midi_messages)
        
        arquivo.save(OUTPUT_FILE_NAME)
        
    def saveExternalMidi(self, user_selected_path: str) -> bool:
        '''
        Copies the generated output.mid to path selected by user
        '''
        try:
            shutil.copy(OUTPUT_FILE_NAME, user_selected_path)
            return True
        except Exception as e:
            return False
        