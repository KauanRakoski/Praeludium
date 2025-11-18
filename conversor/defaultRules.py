
# default execution parameters
DEFAULT_OCTAVE = 4
DEFAULT_VOLUME = 64  # Volume médio (MIDI goes from  0 up to  127)
DEFAULT_BPM = 120 
DEFAULT_TICKS_DURATION = 480 

NOTES = {
    'C4': {'value': 60, 'description': 'Nota Dó'},
    'D4': {'value': 62, 'description': 'Nota Ré'},
    'E4': {'value': 64, 'description': 'Nota Mi'},
    'F4': {'value': 65, 'description': 'Nota Fá'},
    'G4': {'value': 67, 'description': 'Nota Sol'},
    'A4': {'value': 69, 'description': 'Nota Lá'},
    'B4': {'value': 71, 'description': 'Nota Si'},
    'Bb4': {'value': 70, 'description': 'Nota Si Bemol'},
}

INSTRUMENT_MAP = {
    'A': 24,  # Violão com corda de Nylon
    'B': 0,   # Piano Acústico
    'C': 40,  # Violino
    'D': 56,  # Trompete
    'E': 73,  # Flauta
    'F': 14,  # Tubular Bells
    'G': 19,  # órgão eclesiástico
    'H': 48,  # Cordas
    'O': 12, # Marimba
    'E': 13, # Xylophone
    'I': 47, # Harpa
}

def default_rules():
    """
    Returns the complete dictionary with the text-to-music mapping rules. 
    The structure is optimized for use by both the converter and the documentation table.
    """
    rules = {
        # --- MUSICAL NOTES RULES ---
        'A': {'type': 'note', **NOTES['A4']},
        'a': {'type': 'note', **NOTES['A4']}, 
        'B': {'type': 'note', **NOTES['B4']},
        'b': {'type': 'note', **NOTES['B4']}, 
        'C': {'type': 'note', **NOTES['C4']},
        'c': {'type': 'note', **NOTES['C4']}, 
        'D': {'type': 'note', **NOTES['D4']},
        'd': {'type': 'note', **NOTES['D4']}, 
        'E': {'type': 'note', **NOTES['E4']},
        'e': {'type': 'note', **NOTES['E4']}, 
        'F': {'type': 'note', **NOTES['F4']},
        'f': {'type': 'note', **NOTES['F4']}, 
        'G': {'type': 'note', **NOTES['G4']},
        'g': {'type': 'note', **NOTES['G4']}, 
        'H': {'type': 'note', **NOTES['Bb4']},
        'h': {'type': 'note', **NOTES['Bb4']}, 

        # --- PAUSE/SILENCE RULES ---
        ';': {'type': 'pause', 'value': DEFAULT_TICKS_DURATION, 'description': 'Silêncio ou Pausa'},       

        # --- CONTROL RULES ---
        ' ': {'type': 'double_volume', 'value': None, 'description': 'Aumenta o volume para o DOBRO'},
        '?': {'type': 'random_note', 'value': None, 'description': 'Toca uma nota aleatória (A a H)'},

        'O': {'type': 'special_vowel', 'value': None, 'description': 'Se o som anterior era uma nota de A a G, a repete, senão emite um ring sound'},
        'o': {'type': 'special_vowel', 'value': None, 'description': 'Se o som anterior era uma nota de A a G, a repete, senão emite um ring sound'},
        'I': {'type': 'special_vowel', 'value': None, 'description': 'Se o som anterior era uma nota de A a G, a repete, senão emite um ring sound'},
        'i': {'type': 'special_vowel', 'value': None, 'description': 'Se o som anterior era uma nota de A a G, a repete, senão emite um ring sound'},
        'U': {'type': 'special_vowel', 'value': None, 'description': 'Se o som anterior era uma nota de A a G, a repete, senão emite um ring sound'},
        'u': {'type': 'special_vowel', 'value': None, 'description': 'Se o som anterior era uma nota de A a G, a repete, senão emite um ring sound'},

        # --- INSTRUMENT CHANGE RULES (General MIDI) ---
        '!': {'type': 'set_instrument', 'value': 24, 'description': 'Troca para Bandoneon (#24)'},
        '\n': {'type': 'instrument_by_previous', 'value': None, 'description': 'Troca instrumento conforme o caractere anterior'},
        ',': {'type': 'set_instrument', 'value': 114, 'description': 'Troca para Agogô (#114)'},
    }
    
    return rules