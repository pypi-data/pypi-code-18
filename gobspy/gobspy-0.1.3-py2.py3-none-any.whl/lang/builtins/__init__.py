from .builtins import builtins as original_builtins
from ..i18n import translate as t

for k in original_builtins.keys():
    if k[0] != '_':
        try:
            value = original_builtins[k]
            code = '%s = value' % k
            code = '%s = value' % t(k)
            exec(code)
        except e:
            pass

builtins = locals()
