from .defaultRules import default_rules
import mido

# Parâmetros de Execução Padrão
OITAVA_PADRAO = 4
VOLUME_PADRAO = 64  # Volume médio (MIDI vai de 0 a 127)
BPM_PADRAO = 120  # Batidas por minuto
DURACAO_PADRAO_TICKS = 480  # Em MIDI, 480 ticks costuma ser uma semínima em 4/4

class Conversor():
    def __init__(self, rules):
        self.rules = rules
        
        self.instrumento_atual = 0  # 0 é o Piano Acústico no padrão General MIDI
        self.volume_atual = VOLUME_PADRAO
        self.oitava_atual = OITAVA_PADRAO
        self.ultima_nota_tocada = None
        
    def converter_texto(self, texto: str) -> list:
        midi_messages = []
        midi_messages.append(mido.Message('program_change', program=self.instrumento_atual, time=0))
        
        for char in texto:
            # --- 1. Lógica para rules Diretas (A, B, !, ?, etc.) ---
            if char in self.rules:
                regra = self.rules[char]
                tipo_acao = regra['type']
                valor = regra['value']

                if tipo_acao == 'note':
                    nota_real = valor + ((self.oitava_atual - 4) * 12)
                    midi_messages.append(mido.Message('note_on', note=nota_real, velocity=self.volume_atual, time=0))
                    midi_messages.append(mido.Message('note_off', note=nota_real, velocity=self.volume_atual, time=DURACAO_PADRAO_TICKS))
                    self.ultima_nota_tocada = nota_real

                elif tipo_acao == 'pause':
                    if midi_messages:
                        midi_messages[-1].time += valor

                elif tipo_acao == 'set_instrument':
                    self.instrumento_atual = valor
                    midi_messages.append(mido.Message('program_change', program=self.instrumento_atual, time=0))

                elif tipo_acao == 'double_volume':
                    self.volume_atual = min(127, self.volume_atual * 2)

                elif tipo_acao == 'increase_octave':
                    self.oitava_atual += 1
                    if self.oitava_atual > 8:
                        self.oitava_atual = OITAVA_PADRAO
            
            # --- 2. Lógica para rules Contextuais (consoantes, dígitos, etc.) ---
            else:
                if char.isdigit():
                    digito = int(char)
                    if digito % 2 == 0:
                        self.instrumento_atual = (self.instrumento_atual + digito) % 128
                        midi_messages.append(mido.Message('program_change', program=self.instrumento_atual, time=0))
                    else:
                        self.instrumento_atual = 15 # Tubular Bells
                        midi_messages.append(mido.Message('program_change', program=self.instrumento_atual, time=0))

                elif char.isalpha() and char.lower() not in 'aeiou' and char.upper() not in 'ABCDEFGH':
                    if self.ultima_nota_tocada is not None:
                        midi_messages.append(mido.Message('note_on', note=self.ultima_nota_tocada, velocity=self.volume_atual, time=0))
                        midi_messages.append(mido.Message('note_off', note=self.ultima_nota_tocada, velocity=self.volume_atual, time=DURACAO_PADRAO_TICKS))
                    else:
                        if midi_messages:
                            midi_messages[-1].time += DURACAO_PADRAO_TICKS

                else: # ELSE para qualquer outro caractere
                    if self.ultima_nota_tocada is not None:
                        midi_messages.append(mido.Message('note_on', note=self.ultima_nota_tocada, velocity=self.volume_atual, time=0))
                        midi_messages.append(mido.Message('note_off', note=self.ultima_nota_tocada, velocity=self.volume_atual, time=DURACAO_PADRAO_TICKS))
                    else:
                        if midi_messages:
                            midi_messages[-1].time += DURACAO_PADRAO_TICKS
                            
        return midi_messages