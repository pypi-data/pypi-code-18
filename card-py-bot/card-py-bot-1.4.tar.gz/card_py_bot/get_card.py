""" Handler module for parsing the wizzards website for metadata
on magic cards """

import sys
import re

from urllib.request import urlopen
from bs4 import BeautifulSoup
from card_py_bot import get_mana_colors
import html5lib


def grab_html_from_url(url):
    '''
    ARGS:

    RETURNS:
    '''

    try:
        html = urlopen(url)
    except Exception:
        print("ERROR: CHECK URL")

    soup = BeautifulSoup(html, 'html5lib')

    lines = []
    oldline = ""
    for line_prt in soup.get_text():
        if line_prt == "\n":
            oldline = oldline.strip()
            if oldline == "":
                continue
            lines.append(oldline)
            oldline = ""

        oldline = oldline + line_prt

    try:
        start_indx = lines.index("Card Name:")
        end_indx = lines.index("Artist:")
        lines = lines[start_indx:end_indx]
    except Exception:
        return "Error Parsing Card"

    try:
        name_indx = lines.index("Card Name:")
        card_name = lines[name_indx + 1]
    except Exception:
        card_name = "n/a"

    try:
        c_mana_indx = lines.index("Converted Mana Cost:")
        card_c_mana = lines[c_mana_indx + 1]
    except Exception:
        card_c_mana = "Likely no mana"

    try:
        type_indx = lines.index("Types:")
        card_type = lines[type_indx + 1]
        card_type = re.sub('[^a-zA-z]', " ", card_type)
    except Exception:
        card_type = "n/a"

    try:
        text_indx = lines.index("Card Text:")
        card_text = lines[text_indx + 1]
    except Exception:
        card_text = "n/a"

    try:
        ex_indx = lines.index("Expansion:")
        card_expansion = lines[ex_indx + 1]
    except Exception:
        card_expansion = "n/a"

    try:
        rare_indx = lines.index("Rarity:")
        card_rarity = lines[rare_indx + 1]
    except Exception:
        card_rarity = "n/a"

    try:
        num_indx = lines.index("Card Number:")
        card_number = lines[num_indx + 1]
    except Exception:
        card_number = "n/a"

    try:
        (card_mana, img_link_prt) = get_mana_colors.get_mana(url)
    except Exception as error:
        print(error)
        card_mana = "ERROR: Likely no mana"

    card_string = 'Card Name: "{}"\n'.format(card_name)
    card_string += 'Card Mana: {}\n'.format(card_mana)
    card_string += 'Card Converted Mana: "{}"\n'.format(card_c_mana)
    card_string += 'Card Type: "{}"\n'.format(card_type)
    card_string += 'Card Text: {}\n\n'.format(card_text)

    if img_link_prt == "No image link found":
        card_string += img_link_prt
    else:
        card_string += "http://gatherer.wizards.com/" + img_link_prt
    return card_string


if __name__ == "__main__":
    grab_html_from_url(sys.argv[1])
