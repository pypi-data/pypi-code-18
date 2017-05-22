from transpyler.utils.translate import translate_mod as _translate_mod


_es_lib = _translate_mod('es_BR')
globals().update(
    {k: v for k, v in vars(_es_lib).items() if not k.startswith('_')}
)