from .defaultRules import default_rules, NOTES
import mido
import random

OITAVA_PADRAO = 4
VOLUME_PADRAO = 64
BPM_PADRAO = 120
DURACAO_PADRAO_TICKS = 480
MAX_MIDI_VOLUME = 127
MAX_MIDI_PROGRAM = 127
NOTAS_POSSIVEIS = list(NOTES.keys()) #lista notas correspondentes aos caracteres de A até H
CARACTERES_NOTAS = set('ABCDEFG')
TELEPHONE_RING = 124
PIANO = 0

#há sequências de 4 caracteres como "OIT+" e "BPM-" que são consideradas pelo programa como um comando só
COMPOUND_CHARACTER_SIZE = 4 

# Mapeamento de caractere anterior -> instrumento MIDI (General MIDI)
INSTRUMENT_MAP = {
    'A': 24,  # Violão com corda de Nylon
    'B': 0,   # Piano Acústico
    'C': 40,  # Violino
    'D': 56,  # Trompete
    'E': 73,  # Flauta
    'F': 14,  # Tubular Bells
    'G': 19,  # órgão eclesiástico
    'H': 48,  # Cordas 
}


class MidiContext:
    def __init__(self, initial_volume, initial_octave):
        self.instrumento_atual = PIANO  
        self.volume_atual = initial_volume
        self.oitava_atual = initial_octave
        self.ultima_nota_tocada = None
        self.ultimo_caractere = None

    def resetar_oitava(self):
        if self.oitava_atual > 8:
            self.oitava_atual = OITAVA_PADRAO
        elif self.oitava_atual < 1:
            self.oitava_atual = OITAVA_PADRAO
            
    def dobrar_volume(self):
        self.volume_atual = min(MAX_MIDI_VOLUME, self.volume_atual * 2)

    def setar_instrumento(self, valor):
        self.instrumento_atual = valor % (MAX_MIDI_PROGRAM + 1)
        
    def setar_instrumento_tubular_bells(self):
        self.instrumento_atual = 15
        
class Conversor():
    def __init__(self, rules):
        self.rules = rules
        
        self.action_handlers = {
            'note': self._handle_note,
            'pause': self._handle_pause,
            'set_instrument': self._handle_set_instrument,
            'double_volume': self._handle_double_volume,
            'increase_octave': self._handle_increase_octave,
            'random_note': self._handle_random_note,
            'special_vowel': self._handle_special_vowel,
            'instrument_by_previous': self._handle_instrument_by_previous,

        }
        
    '''def converter_texto(self, texto: str, initial_volume: int, initial_octave: int) -> list:
        context = MidiContext(initial_volume, initial_octave)
        midi_messages = []
        
        midi_messages.append(mido.Message('program_change', 
                                          program=context.instrumento_atual, 
                                          time=0))
        
        for char in texto:
            self._processar_char(char, context, midi_messages)
            context.ultimo_caractere = char  # guarda o último caractere processado
        
        return midi_messages'''
            
    def converter_texto(self, texto: str, initial_volume: int, initial_octave: int) -> list:
        context = MidiContext(initial_volume, initial_octave)
        midi_messages = []
        
        midi_messages.append(mido.Message('program_change', 
                                          program=context.instrumento_atual, 
                                          time=0))
        
        i = 0

        while(i < len(texto)):
            
            if i+(COMPOUND_CHARACTER_SIZE-1) < len(texto):
                seq = texto[i:i+COMPOUND_CHARACTER_SIZE]
                if seq == "OIT+" or seq == "OIT-":
                    self._handle_octave_change_sequence(seq[COMPOUND_CHARACTER_SIZE-1], context)
                    i += COMPOUND_CHARACTER_SIZE
                    continue

                elif seq == "BPM+" or seq == "BPM-":
                    self._handle_bpm_change_sequence(seq[COMPOUND_CHARACTER_SIZE-1], context)
                    i += COMPOUND_CHARACTER_SIZE
                    continue

            char = texto[i]
            self._processar_char(char, context, midi_messages)
            context.ultimo_caractere = char
            i += 1

        return midi_messages
    
    def _processar_char(self, char: str, context: MidiContext, messages: list):
        if char in self.rules:
            regra = self.rules[char]
            tipo_acao = regra.get('type')
            valor = regra.get('value')
            
            handler = self.action_handlers.get(tipo_acao)
            
            if handler:
                handler(context, valor, messages)
            else:
                print(f"Aviso: Ação desconhecida '{tipo_acao}' para o caractere '{char}'.")
                
        else:
            self._handle_contextual_char(char, context, messages)
            
    def _handle_note(self, context: MidiContext, valor: int, messages: list):
        nota_real = valor + ((context.oitava_atual - 4) * 12)
        messages.append(mido.Message('note_on', note=nota_real, velocity=context.volume_atual, time=0))
        messages.append(mido.Message('note_off', note=nota_real, velocity=context.volume_atual, time=DURACAO_PADRAO_TICKS))
        context.ultima_nota_tocada = nota_real

    def _handle_pause(self, context: MidiContext, valor: int, messages: list):
        if messages:
            messages[-1].time += valor

    def _handle_set_instrument(self, context: MidiContext, valor: int, messages: list):
        context.setar_instrumento(valor)
        messages.append(mido.Message('program_change', program=context.instrumento_atual, time=0))

    def _handle_double_volume(self, context: MidiContext):
        context.dobrar_volume()

    def _handle_increase_octave(self, context: MidiContext):
        context.oitava_atual += 1
        context.resetar_oitava()

    def _handle_decrease_octave(self, context: MidiContext):
        context.oitava_atual -= 1
        context.resetar_oitava
    
    '''def _handle_decrease_bpm(self, context: MidiContext, valor, messages: list):
        context.oitava_atual -= 1
        context.resetar_oitava
    
    def _handle_increase_bpm(self, context: MidiContext, valor, messages: list):
        context.
        context.resetar_oitava'''
    

    def _handle_contextual_char(self, char: str, context: MidiContext, messages: list):
        """ Processa caracteres que NÃO estão no mapa de regras. """
        
        if char.isdigit():
            digito = int(char)
            if digito % 2 == 0:
                context.setar_instrumento(context.instrumento_atual + digito)
                messages.append(mido.Message('program_change', program=context.instrumento_atual, time=0))
            else:
                context.setar_instrumento_tubular_bells()
                messages.append(mido.Message('program_change', program=context.instrumento_atual, time=0))
        
        elif char.isalpha() and char.lower() not in 'aeiou' and char.upper() not in 'ABCDEFGH':
            self._handle_repeat_or_pause(context, messages)
            
        else:
            self._handle_repeat_or_pause(context, messages)

    def _handle_repeat_or_pause(self, context: MidiContext, messages: list):
        if context.ultima_nota_tocada is not None:
            messages.append(mido.Message('note_on', note=context.ultima_nota_tocada, velocity=context.volume_atual, time=0))
            messages.append(mido.Message('note_off', note=context.ultima_nota_tocada, velocity=context.volume_atual, time=DURACAO_PADRAO_TICKS))
        else:
            if messages:
                messages[-1].time += DURACAO_PADRAO_TICKS

    def _handle_random_note(self, context: MidiContext, valor, messages: list):
        
        nota_escolhida = random.choice(NOTAS_POSSIVEIS)
        valor_midi = NOTES[nota_escolhida]['value']

        nota_real = valor_midi + ((context.oitava_atual - 4) * 12)

        messages.append(mido.Message('note_on', note=nota_real, velocity=context.volume_atual, time=0))
        messages.append(mido.Message('note_off', note=nota_real, velocity=context.volume_atual, time=DURACAO_PADRAO_TICKS))

        context.ultima_nota_tocada = nota_real

    def _handle_special_vowel(self, context: MidiContext, valor, messages: list):
        
        if context.ultimo_caractere in CARACTERES_NOTAS:
            # Repetir a última nota
            messages.append(mido.Message('note_on', note=context.ultima_nota_tocada, velocity=context.volume_atual, time=0))
            messages.append(mido.Message('note_off', note=context.ultima_nota_tocada, velocity=context.volume_atual, time=DURACAO_PADRAO_TICKS))
        else:
            context.setar_instrumento(TELEPHONE_RING)
            messages.append(mido.Message('program_change', program=context.instrumento_atual, time=0))

            messages.append(mido.Message('note_on', note=60, velocity=context.volume_atual, time=0))
            messages.append(mido.Message('note_off', note=60, velocity=context.volume_atual, time=DURACAO_PADRAO_TICKS))

            #restaura para instrumnento padrão
            context.setar_instrumento(PIANO)
            messages.append(mido.Message('program_change', program=context.instrumento_atual, time=0))
    
    def _handle_instrument_by_previous(self, context: MidiContext, valor, messages: list):
        """
        Muda o instrumento com base no caractere anterior.
        Exemplo: A\n → violão, B\n → piano etc.
        """
        ultimo_caractere = context.ultimo_caractere

        if ultimo_caractere in INSTRUMENT_MAP:
            context.setar_instrumento(INSTRUMENT_MAP[ultimo_caractere.upper()])
            messages.append(mido.Message('program_change', program=context.instrumento_atual, time=0))
        else:
            # Se não há caractere anterior válido, mantém o instrumento atual
            if messages:
                messages[-1].time += DURACAO_PADRAO_TICKS

    def _handle_octave_change_sequence(self, signal, context : MidiContext):
        if signal == '+':
            self._handle_increase_octave(context)
        else:
            self._handle_decrease_octave(context)

    def _handle_bpm_change_sequence(self, signal, context : MidiContext):
        if signal  == '+':
           # self._handle_increase_bpm
           print("mais")
        else:
            #self._handle_decrease_bpm
            print("menos")