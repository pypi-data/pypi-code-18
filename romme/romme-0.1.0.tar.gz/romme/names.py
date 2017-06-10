# -*- coding: UTF-8 -*-

import re
from unidecode import unidecode

from romme.romans import decimal_to_roman


def sanitize_name(s):
    s = re.sub(r"\s+", " ", s)
    s = unidecode(s.strip().lower())
    s = re.sub(r"[.,;']+", "", s)
    return s

class Label:
    def __init__(self, label):
        self.label = label
        self.sanitized = sanitize_name(label)

    def __str__(self):
        return self.label

months = (
    Label(""),
    Label("Vendémiaire"),
    Label("Brumaire"),
    Label("Frimaire"),
    Label("Nivôse"),
    Label("Pluviôse"),
    Label("Ventôse"),
    Label("Germinal"),
    Label("Floréal"),
    Label("Prairial"),
    Label("Messidor"),
    Label("Thermidor"),
    Label("Fructidor"),
)

sans_culottides = (
    Label(""),
    Label("de la vertu"),
    Label("du génie"),
    Label("du travail"),
    Label("de l'opinion"),
    Label("des récompenses"),
    Label("de la révolution"),
)


def republican_year_string(year):
    return decimal_to_roman(year)


def republican_day_string(year, month, day):
    year_string = republican_year_string(year)

    if month >= len(months):
        # sans-culottide
        return "jour %s, an %s" % (sans_culottides[day], year_string)

    return "%d %s, an %s" % (day, months[month], year_string)
