from requests.compat import urljoin

ANIDEX_URL = 'https://anidex.info'
SEARCH_URL = urljoin(ANIDEX_URL, '/ajax/page.ajax.php')
MAGNET_REGEX = r"href=\"(magnet[^\"]+)"
LIKES_REGEX = r"title=\"([0-9]+)\ likes"
HEADERS = {'X-Requested-With': 'XMLHttpRequest'}
CATEGORIES = {
    'ANIME': 1,
    'DRAMA': 2,
    'GAMES': 3,
    'LN': 4,
    'MANGA': 5,
    'MUSIC': 6,
    'OTHER': 7,
}
FILTER_MODE_VALUES = [1, 2]
LANGUAGES = {
    'ALL': 0,
    'ARABIC': 19,
    'BENGALI': 22,
    'BULGARIAN': 14,
    'CHINESE-SIMPLIFIED': 21,
    'CZECH': 24,
    'DANISH': 20,
    'DUTCH': 5,
    'ENGLISH': 1,
    'FINNISH': 11,
    'FRENCH': 10,
    'GERMAN': 8,
    'GREEK': 13,
    'HUNGARIAN': 9,
    'INDONESIAN': 27,
    'ITALIAN': 6,
    'JAPANESE': 23,
    'KOREAN': 28,
    'MONGOLIAN': 25,
    'POLISH': 3,
    'PORTUGUESE-BRAZIL': 16,
    'PORTUGUESE-PORTUGAL': 17,
    'ROMANIAN': 2,
    'RUSSIAN': 7,
    'SERBO-CROATIAN': 4,
    'SPANISH-LATAM': 29,
    'SPANISH-SPAIN': 15,
    'SWEDISH': 18,
    'TURKISH': 26,
    'VIETNAMESE': 12
}
