# importa funcao de mapeamento e as notas musicais
from .defaultRules import default_rules, NOTES, INSTRUMENT_MAP

import mido
import random

DEFAULT_OCTAVE = 4
DEFAULT_VOLUME = 64
DEFAULT_BPM = 120
DEFAULT_TICKS_DURATION = 480
MAX_MIDI_VOLUME = 127
MAX_MIDI_PROGRAM = 127
POSSIBLE_NOTES = list(NOTES.keys())
NOTE_CHARACTERS = set('ABCDEFG')
TELEPHONE_RING = 124
PIANO = 0

COMPOUND_CHARACTER_SIZE = 4 


class MidiContext:

    # Arbitrary values
    MIN_BPM = 30
    MAX_BPM = 300
    
    def __init__(self, initial_volume, initial_octave, initial_bpm):
        self.current_instrument = PIANO  
        self.current_volume = initial_volume
        self.current_octave = initial_octave
        self.current_bpm = initial_bpm
        self.last_played_note = None
        self.last_character = None
        self.pending_pause_ticks = 0

    def reset_octave(self):
        if self.current_octave > 8:
            self.current_octave = DEFAULT_OCTAVE
        elif self.current_octave < 1:
            self.current_octave = DEFAULT_OCTAVE
            
    def double_volume(self):
        self.current_volume = min(MAX_MIDI_VOLUME, self.current_volume * 2)

    def set_instrument(self, valor):
        self.current_instrument = valor % (MAX_MIDI_PROGRAM + 1)
        
    def get_instrument(self):
        return self.current_instrument
        
    def set_instrument_tubular_bells(self):
        self.current_instrument = 15
    
    def adjust_bpm(self, change_value:int):
        self.current_bpm += change_value
        self.current_bpm = max(self.MIN_BPM, min(self.MAX_BPM, self.current_bpm))
        
    def zero_pending_time(self):
        self.pending_pause_ticks = 0
        
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
            
    def convert_text(self, texto: str, context: MidiContext) -> list:
        """
        Given a text and initial context, converts the text using specified rules to midi
        """
        midi_messages = []
        
        midi_messages.append(mido.Message('program_change', 
                                          program=context.current_instrument, 
                                          time=0))
        
        initial_tempo = mido.bpm2tempo(context.current_bpm)
        midi_messages.append(mido.MetaMessage('set_tempo', tempo=initial_tempo, time=0))
        
        i = 0
        while(i < len(texto)):
            if i+(COMPOUND_CHARACTER_SIZE-1) < len(texto):
                seq = texto[i:i+COMPOUND_CHARACTER_SIZE]
                if seq == "OIT+" or seq == "OIT-":
                    self._handle_octave_change_sequence(seq[COMPOUND_CHARACTER_SIZE-1], context)
                    i += COMPOUND_CHARACTER_SIZE
                    continue

                elif seq == "BPM+" or seq == "BPM-":
                    self._handle_bpm_change_sequence(seq[COMPOUND_CHARACTER_SIZE-1], context, midi_messages)
                    i += COMPOUND_CHARACTER_SIZE
                    continue
            
            char = texto[i]
            self._process_char(char, context, midi_messages)
            context.last_character = char
            i += 1

        return midi_messages
    
    def _process_char(self, char: str, context: MidiContext, messages: list):
        if char in self.rules:
            regra = self.rules[char]
            
            tipo_acao = regra.get('type')
            valor = regra.get('value')
            
            handler = self.action_handlers.get(tipo_acao)
            
            if handler:
                handler(context, valor, messages)
            else:
                print(f"Aviso: Ação desconhecida '{tipo_acao}' para o caractere '{char}'.")
            
    def _handle_note(self, context: MidiContext, valor: int, messages: list):
        nota_real = valor + ((context.current_octave - 4) * 12)
        messages.append(mido.Message('note_on', note=nota_real, velocity=context.current_volume, time=context.pending_pause_ticks))
        context.zero_pending_time()
        messages.append(mido.Message('note_off', note=nota_real, velocity=context.current_volume, time=DEFAULT_TICKS_DURATION))
        context.last_played_note = nota_real

    def _handle_pause(self, context: MidiContext, valor: int, messages: list):
        context.pending_pause_ticks += DEFAULT_TICKS_DURATION

    def _handle_set_instrument(self, context: MidiContext, valor: int, messages: list):
        context.set_instrument(valor)
        messages.append(mido.Message('program_change', program=context.current_instrument, time=0))

    def _handle_double_volume(self, context: MidiContext, valor, messages):
        context.double_volume()

    def _handle_increase_octave(self, context: MidiContext):
        context.current_octave += 1
        context.reset_octave()

    def _handle_decrease_octave(self, context: MidiContext):
        context.current_octave -= 1
        context.reset_octave()    

    def _handle_repeat_or_pause(self, context: MidiContext, messages: list):
        if context.last_played_note is not None:
            messages.append(mido.Message('note_on', note=context.last_played_note, velocity=context.current_volume, time=context.pending_pause_ticks))
            messages.append(mido.Message('note_off', note=context.last_played_note, velocity=context.current_volume, time=DEFAULT_TICKS_DURATION))
        else:
            if messages:
                messages[-1].time += DEFAULT_TICKS_DURATION

    def _handle_random_note(self, context: MidiContext, valor, messages: list):
        
        nota_escolhida = random.choice(POSSIBLE_NOTES)
        valor_midi = NOTES[nota_escolhida]['value']

        nota_real = valor_midi + ((context.current_octave - 4) * 12)

        messages.append(mido.Message('note_on', note=nota_real, velocity=context.current_volume, time=context.pending_pause_ticks))
        messages.append(mido.Message('note_off', note=nota_real, velocity=context.current_volume, time=DEFAULT_TICKS_DURATION))

        context.last_played_note = nota_real

    def _handle_special_vowel(self, context: MidiContext, valor, messages: list):
        
        if context.last_character in NOTE_CHARACTERS:
            messages.append(mido.Message('note_on', note=context.last_played_note, velocity=context.current_volume, time=context.pending_pause_ticks))
            messages.append(mido.Message('note_off', note=context.last_played_note, velocity=context.current_volume, time=DEFAULT_TICKS_DURATION))
        else:
            previous_instrument = context.get_instrument()
            context.set_instrument(TELEPHONE_RING)
            messages.append(mido.Message('program_change', program=context.current_instrument, time=context.pending_pause_ticks))

            messages.append(mido.Message('note_on', note=60, velocity=context.current_volume, time=context.pending_pause_ticks))
            messages.append(mido.Message('note_off', note=60, velocity=context.current_volume, time=DEFAULT_TICKS_DURATION))

            context.set_instrument(previous_instrument)
            messages.append(mido.Message('program_change', program=context.current_instrument, time=context.pending_pause_ticks))
    
    def _handle_instrument_by_previous(self, context: MidiContext, valor, messages: list):
        """
        Changes instrument based on last char.
        Example A\n -> guitar, B\n -> piano
        """
        last_character = context.last_character

        if last_character in INSTRUMENT_MAP:
            context.set_instrument(INSTRUMENT_MAP[last_character.upper()])
            messages.append(mido.Message('program_change', program=context.current_instrument, time=0))
        else:
            if messages:
                messages[-1].time += DEFAULT_TICKS_DURATION

    def _handle_octave_change_sequence(self, signal, context : MidiContext):
        if signal == '+':
            self._handle_increase_octave(context)
        else:
            self._handle_decrease_octave(context)

    def _handle_bpm_change_sequence(self, signal, context : MidiContext, messages: list):
        if signal  == '+':
           context.adjust_bpm(80)
        else:
            context.adjust_bpm(-80)
            
        novo_tempo = mido.bpm2tempo(context.current_bpm)
        messages.append(mido.MetaMessage('set_tempo', tempo=novo_tempo, time=0))