#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Get a random font name as string, useful for HTML/CSS styling."""


# This groups have been tested on HTML/CSS with one each other,
# they look pretty good on all combinations, we are not Designers,
# but this is useful for quick templating and boilerplates styling.
# They are all Open Source from Trending+Popular category on google fonts.


from random import choice


def get_random_handwriting_font():
    """Get a random handwriting font name as string. For Titles/SubTitles."""
    return choice((
        "Molle", "Pacifico", "Yellowtail", "Dekko", "Courgette", "Satisfy",
        "Cookie", "Handlee", "Sacramento", "Tangerine", "Damion", "Kalam",
        "Neucha", "Calligraffitti", "Rancho", "Allura", "Niconne", "Rochester",
        "Parisienne", "Merienda", "Caveat", "Tillana", "Italianno", "Sofia",
        "Arizonia", "Montez", "Sriracha", "Delius", "Qwigley", "Itim", "Julee",
        "Quintessential", "Fondamento", "Ruthie", "Condiment", "Amita",
        "Yesteryear", "Aladin", "Norican", "Engagement", "Stalemate", "Meddon",
        "Vibur", "Bilbo", "Redressed", "Devonshire", "Kavivanar", "Kristi"))


def get_random_mono_font():
    """Get a random monospaced font name as string. Few fonts. For Code."""
    return choice((
        "Inconsolata", "Cousine", "Roboto Mono", "Source Code Pro",
        "Droid Sans Mono", "Space Mono", "PT Mono", "Ubuntu Mono", "Nova Mono",
        "Share Tech Mono", "Anonymous Pro", "Oxygen Mono", "Cutive Mono",
        "Fira Mono"))


def get_random_display_font():
    """Get a random decorative display cosmetic font name as string.For Fun."""
    return choice((
        "Mirza", "Lobster", "Buda", "Comfortaa", "Righteous", "Chewy", "Allan",
        "Audiowide", "Boogaloo", "Playball", "Bangers", "Bevan", "Shrikhand",
        "Coda", "Share", "Overlock", "Arbutus", "Limelight", "Pompiere",
        "Monoton", "Graduate", "Lalezar", "Farsan", "Bungee", "Rakkas", "Atma",
        "Mogra", "Slackey", "Forum", "Kavoon", "Fruktur", "Gruppo", "Baumans",
        "Unkempt", "Corben", "Crushed", "Kranky", "Skranji", "Oregano", "Sail",
        "Knewave", "Sniglet", "Shojumaru", "Voces", "Revalia", "Megrim",
        "Lemonada", "Lemon", "Coiny", "Baloo", "Frijole", "Salsa", "Simonetta",
        "Wallpoet", "McLaren", "Amarante", "Iceland", "Chonburi", "Dynalight",
        "Galada", "Metamorphous", "Ribeye", "Milonga", "Flamenco", "Elsie",
        "Chicle", "Paprika", "Piedra", "Akronim", "Iceberg", "Oldenburg",
        "Offside", "Galindo", "Wellfleet", "Sarina", "MedievalSharp", "Chango",
        "Peralta", "Miniver", "Trochut", "Lancelot", "Risque", "Gorditas",
        "Kenia", "Margarine", "Underdog", "Smythe", "Ranchers", "Astloch",
        "Fascinate", "Miltonian", "Warnes", "Combo", "Spirax", "Aubrey",
        "Flavors", "Macondo", "Federant", "Geostar", "Sevillana", "Unlock"))


def get_random_sans_font():
    """Get a random sans font name as string. These are for serious stuff."""
    return choice((
        "Roboto", "Oswald", "Montserrat", "Raleway", "Ubuntu", "Arimo", "Muli",
        "Dosis", "Oxygen", "Nunito", "Hind", "Cabin", "Catamaran", "Abel",
        "Asap", "Quicksand", "Karla", "Signika", "Questrial", "Exo", "Acme",
        "Orbitron", "Rubik", "Monda", "BenchNine", "ABeeZee", "Gudea", "Teko",
        "Armata", "Economica", "Ruda", "Aclonica", "Sintony", "Yantramanav",
        "Voltaire", "Amaranth", "Cantarell", "Rambla", "Varela", "Aldrich",
        "Antic", "Actor", "Nobile", "Electrolize", "Heebo", "Homenaje", "Jura",
        "Molengo", "Viga", "Syncopate", "Basic", "Candal", "Michroma", "Carme",
        "Marmelad", "Telex", "Chivo", "Spinnaker", "Convergence", "Allerta",
        "Marvel", "Quantico", "Puritan", "Magra", "Rosario", "Mako", "Asul",
        "Anaheim", "Tauri", "Metrophobic", "Strait", "Belleza", "Inder", "Geo",
        "Capriola", "Assistant", "Prompt", "Lekton", "Imprima", "Orienta",
        "Gafata", "Shanti", "Federo", "Englebert", "Rationale", "Numans",
        "Cagliostro", "Ruluko", "Snippet", "Fresca", "Galdeano", "Lato"))


def get_random_serif_font():
    """Get a random serif font name as string. These are for serious stuff."""
    return choice((
        "Bitter", "Arvo", "Alegreya", "Vollkorn", "Rokkitt", "Cinzel", "Ovo",
        "Domine", "Sanchez", "Vidaloka", "Tinos", "Arapey", "Cardo", "Kreon",
        "Glegoo", "Neuton", "Adamina", "Volkhov", "Copse", "Alice", "Prata",
        "Enriqueta", "Prociono", "Kameron", "Martel", "Lusitana", "Average",
        "Andada", "Lustria", "Marcellus", "Cutive", "Halant", "Rasa", "Mate",
        "Coustard", "BioRhyme", "Pridi", "Trocchi", "Radley", "Caudex", "Yrsa",
        "Rufina", "Karma", "Quando", "Alike", "Bentham", "Poly", "Brawler",
        "Judson", "Cormorant", "Fenix", "Kurale", "Gabriela", "Unna", "Junge",
        "Belgrano", "Cambo", "Tienne", "Balthazar", "Italiana", "Podkova",
        "Amethysta", "Ledger", "Buenard", "Habibi", "Esteban", "Inika", "Sura",
        "Artifika", "Rosarivo", "Stoke", "Almendra", "Laila", "Kadwa",
        "Petrona", "Trykker", "Montaga", "Sahitya", "Asar", "Peddana"))


def get_random_font():
    """Get a random font name as string. Any kind of font."""
    return choice((get_random_handwriting_font(), get_random_mono_font(),
                   get_random_display_font(), get_random_sans_font(),
                   get_random_serif_font()))
