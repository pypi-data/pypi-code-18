import sys

from transpyler import Transpyler
from transpyler.utils import pretty_callable
from . import __version__
from .keywords import TRANSLATIONS, SEQUENCE_TRANSLATIONS, ERROR_GROUPS


class PytunolTranspyler(Transpyler):
    """
    Pytuñol support.
    """

    name = 'pytunol'
    display_name = 'Pytuñol'
    translations = dict(TRANSLATIONS)
    translations.update(SEQUENCE_TRANSLATIONS)
    error_dict = ERROR_GROUPS
    lang = 'es_BR'

    def update_user_ns(self, ns):
        @pretty_callable(
            'Escribid "salir ()" para finalizar la ejecución.',
            autoexec=True, autoexec_message='Adiós! ;-)'
        )
        def sair():
            """
            Finaliza la ejecución del terminal de Pytuñol.
            """

            ns['exit']()

        ns['sair'] = sair


pytunol_transpyler = PytunolTranspyler()
PytunolTranspyler.banner = \
    r'''pytunol %s
Python %s

Bienvenido a Pytuñol, un Python en español con acento brasileño.''' \
    % (__version__, sys.version.splitlines()[0])

#TODO: Escribid "ayuda()", "licencia()" o "tutorial()" para más información.
