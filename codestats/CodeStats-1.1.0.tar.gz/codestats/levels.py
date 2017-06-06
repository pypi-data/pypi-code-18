import math

LEVEL_FACTOR = 0.025


def calculate_level(experience: int, level_factor: float=LEVEL_FACTOR) -> int:
    """
    Calculate the current level based on the provided experience and level factor. The
     same formula is used as the official API / website.

    :param experience: The experience to calculate the level of
    :param level_factor: The level factor to use, defaults to ``LEVEL_FACTOR`` (0.025)
    :return:The level as an integer
    """
    return int(math.floor(level_factor * math.sqrt(experience)))


def calculate_next_level_xp(experience: int=None, level: int=None, level_factor: float=LEVEL_FACTOR) -> int:
    """
    Calculate how much experience is needed to reach the next level. If a level if provided
     this used, otherwise the provided experience is used to first calculate the level.
    :param experience: The experience to calculate the level if no level was provided
    :param level: The current level
    :param level_factor: The level factor to use, defaults to ``LEVEL_FACTOR`` (0.025)
    :return: The experience needed as an integer
    :raise ValueError: If ``experience`` and ``level`` are both ``None``.
    """
    if level is None and experience is not None:
        level = calculate_level(experience)
    elif level is None and experience is None:
        raise ValueError("'Experience' and 'level' cannot both be None")

    return int(math.pow(math.ceil((level + 1) / level_factor), 2))


def calculate_progress(experience: int) -> float:
    """
    Calculate the progress to the next level as a percentage.
    :param experience: The current experience
    :return: The percentage as a float
    """
    level = calculate_level(experience)
    current_level_xp = calculate_next_level_xp(level=level - 1)
    next_level_xp = calculate_next_level_xp(level=level)

    have_xp = experience - current_level_xp
    needed_xp = next_level_xp - current_level_xp

    return (have_xp / needed_xp) * 100
