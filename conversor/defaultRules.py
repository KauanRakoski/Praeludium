
# Parâmetros de Execução Padrão
OITAVA_PADRAO = 4
VOLUME_PADRAO = 64  # Volume médio (MIDI vai de 0 a 127)
BPM_PADRAO = 120  # Batidas por minuto
DURACAO_PADRAO_TICKS = 480  # Em MIDI, 480 ticks costuma ser uma semínima em 4/4

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

# Needs to be created in a more consistent way, just boilerplate for testing
def default_rules():
    """
    Retorna o dicionário completo com as regras de mapeamento de texto para música.
    A estrutura é otimizada para ser usada tanto pelo conversor quanto pela
    tabela de documentação.
    """
    rules = {
        # --- REGRAS DE NOTAS MUSICAIS ---
        'A': {'type': 'note', **NOTES['A4']},
        'B': {'type': 'note', **NOTES['B4']},
        'C': {'type': 'note', **NOTES['C4']},
        'D': {'type': 'note', **NOTES['D4']},
        'E': {'type': 'note', **NOTES['E4']},
        'F': {'type': 'note', **NOTES['F4']},
        'G': {'type': 'note', **NOTES['G4']},
        'H': {'type': 'note', **NOTES['Bb4']},

        # --- REGRAS DE PAUSA/SILÊNCIO ---
        'a': {'type': 'pause', 'value': DURACAO_PADRAO_TICKS, 'description': 'Silêncio ou Pausa'},
        'b': {'type': 'pause', 'value': DURACAO_PADRAO_TICKS, 'description': 'Silêncio ou Pausa'},
        'c': {'type': 'pause', 'value': DURACAO_PADRAO_TICKS, 'description': 'Silêncio ou Pausa'},
        'd': {'type': 'pause', 'value': DURACAO_PADRAO_TICKS, 'description': 'Silêncio ou Pausa'},
        'e': {'type': 'pause', 'value': DURACAO_PADRAO_TICKS, 'description': 'Silêncio ou Pausa'},
        'f': {'type': 'pause', 'value': DURACAO_PADRAO_TICKS, 'description': 'Silêncio ou Pausa'},
        'g': {'type': 'pause', 'value': DURACAO_PADRAO_TICKS, 'description': 'Silêncio ou Pausa'},
        'h': {'type': 'pause', 'value': DURACAO_PADRAO_TICKS, 'description': 'Silêncio ou Pausa'},

        # --- REGRAS DE CONTROLE ---
        ' ': {'type': 'double_volume', 'value': None, 'description': 'Aumenta o volume para o DOBRO'},
        '?': {'type': 'increase_octave', 'value': 1, 'description': 'Aumenta UMA oitava'},
        '.': {'type': 'increase_octave', 'value': 1, 'description': 'Aumenta UMA oitava'},

        # --- REGRAS DE MUDANÇA DE INSTRUMENTO (General MIDI) ---
        '!': {'type': 'set_instrument', 'value': 24, 'description': 'Troca para Bandoneon (#24)'},
        'O': {'type': 'set_instrument', 'value': 110, 'description': 'Troca para Gaita de Foles (#110)'},
        'o': {'type': 'set_instrument', 'value': 110, 'description': 'Troca para Gaita de Foles (#110)'},
        'I': {'type': 'set_instrument', 'value': 110, 'description': 'Troca para Gaita de Foles (#110)'},
        'i': {'type': 'set_instrument', 'value': 110, 'description': 'Troca para Gaita de Foles (#110)'},
        'U': {'type': 'set_instrument', 'value': 110, 'description': 'Troca para Gaita de Foles (#110)'},
        'u': {'type': 'set_instrument', 'value': 110, 'description': 'Troca para Gaita de Foles (#110)'},
        '\n': {'type': 'set_instrument', 'value': 123, 'description': 'Troca para Ondas do Mar (#123)'},
        ';': {'type': 'set_instrument', 'value': 15, 'description': 'Troca para Tubular Bells (#15)'},
        ',': {'type': 'set_instrument', 'value': 114, 'description': 'Troca para Agogô (#114)'},
    }
    
    return rules