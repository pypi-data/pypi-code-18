import random

def to_jeje(some_string: str):
    """
    converts any string to an equivalent
    Jejemon-inspired counterpart.
    """
    some_string += ' gan3rn phouwz'
    some_string = some_string.replace(
        'o', '0').replace('e', '3').replace(
            'a', '4'
        )
    some_string = "".join(
        random.choice([k.upper(), k]) for k in some_string)
    return some_string
