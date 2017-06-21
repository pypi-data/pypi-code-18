
norm_id_list = [
    ":gm:",
    ":rm:",
    ":um:",
    ":bm:",
    ":wm:",
    ":upm:",
    ":rpm:",
    ":gpm:",
    ":bpm:",
    ":wpm:",
    ":1m:",
    ":2m:",
    ":3m:",
    ":4m:",
    ":5m:",
    ":6m:",
    ":7m:",
    ":8m:",
    ":9m:",
    ":10m:",
    ":11m:",
    ":12m:",
    ":13m:",
    ":14m:",
    ":15m:",
    ":16m:",
    ":1000000m:",
    ":bgm:",
    ":rwm:",
    ":gum:",
    ":urm:",
    ":wbm:",
    ":wum:",
    ":ubm:",
    ":brm:",
    ":rgm:",
    ":gwm:",
    ":2wm:",
    ":2gm:",
    ":2bm:",
    ":2rm:",
    ":2bm:",
    ":Tap:",
    ":Untap:",
    ":Energy:"
]


def print_ids():
    """
    return a string of all the mana ids (in order) for config setup in discord
    """
    config_string = ("RECOPY THIS AND PASTE THIS INTO CHAT THEN TAKE THE" +
                     "OUTPUT AND SAVE IT INTO CONFIG.TXT\n")
    config_string = '?save_setup\n'
    for raw_id in norm_id_list:
        config_string += ("\\\\" + raw_id + "\n")

    return config_string
