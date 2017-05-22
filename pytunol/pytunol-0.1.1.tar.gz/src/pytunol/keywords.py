import collections
import keyword


TRANSLATIONS = {
    # Loops
    'para': 'for',
    'para_cada': 'for',
    'hasta': 'ate',
    'siga': 'pass',
    'romper': 'break',
    'mientras': 'while',

    # Conditions
    'si': 'if',
    'o_si': 'elif',
    'si_no': 'else',

    # Singleton values
    'Falso': 'False',
    'falso': 'False',
    'Nulo': 'None',
    'nulo': 'None',
    'Verdadero': 'True',
    'verdadero': 'True',

    # Operators
    'es': 'is',
    'en': 'in',
    'no': 'not',
    'o': 'or',
    'y': 'and',
    'como': 'as',
    'suprimir': 'del',

    # Function/class definitions
    'clase': 'class',
    'definir': 'def',
    'defina': 'def',
    'función': 'def', 'funcion': 'def',
    'generar': 'yield',
    'gestiona': 'yield',
    'regresar': 'return',
    'volver': 'return',

    # Error
    'intentar': 'try',
    'intente': 'try',
    'excepción': 'except', 'excepcion': 'except',
    'finalmente': 'finally',
    'levantar_error': 'raise',
    'levante_error': 'raise',

    # Other
    'importar': 'import',
    'importe': 'import',
    'con': 'with',
}

SEQUENCE_TRANSLATIONS = {
    # Block ending
    ('haga', ':'): ':',
    ('hacer', ':'): ':',

    # Loops
    ('para', 'cada'): 'for',

    # Conditions
    ('entonces', 'haga', ':'): ':',
    ('entonces', ':'): ':',
    ('o', 'si'): 'elif',
    ('ou', 'entao', 'se'): 'elif',
    ('ou', 'si'): 'elif',
    ('ou', 'si'): 'elif',
    ('si', 'no'): 'else',

    # Definitions
    ('definir', 'función'): 'def',
    ('definir', 'funcion'): 'def',
    ('defina', 'función'): 'def',
    ('defina', 'funcion'): 'def',
    ('definir', 'clase'): 'class',
    ('defina', 'clase'): 'class',
}

ERROR_GROUPS = collections.OrderedDict(
    (x, 'Repetición no válida: %s' % (' '.join(x)))
    for x in [
        ('haga', 'haga'), ('haga', 'hacer'), ('hacer', 'haga'),
        ('entonces', 'entonces'),
    ]
)
