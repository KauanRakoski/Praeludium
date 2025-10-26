from .defaultRules import default_rules
import mido

OITAVA_PADRAO = 4
VOLUME_PADRAO = 64
BPM_PADRAO = 120
DURACAO_PADRAO_TICKS = 480
MAX_MIDI_VOLUME = 127
MAX_MIDI_PROGRAM = 127

class MidiContext:
    def __init__(self, initial_volume, initial_octave):
        self.instrumento_atual = 0  # Piano Acústico
        self.volume_atual = initial_volume
        self.oitava_atual = initial_octave
        self.ultima_nota_tocada = None

    def resetar_oitava(self):
        if self.oitava_atual > 8:
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
        }
        
    def converter_texto(self, texto: str, initial_volume: int, initial_octave: int) -> list:
        context = MidiContext(initial_volume, initial_octave)
        midi_messages = []
        
        midi_messages.append(mido.Message('program_change', 
                                          program=context.instrumento_atual, 
                                          time=0))
        
        for char in texto:
            self._processar_char(char, context, midi_messages)
            
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

    def _handle_double_volume(self, context: MidiContext, valor, messages: list):
        context.dobrar_volume()

    def _handle_increase_octave(self, context: MidiContext, valor, messages: list):
        context.oitava_atual += 1
        context.resetar_oitava()

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