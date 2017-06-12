import json
from os import path

from .emoji_char import EmojiChar

with open(path.join(path.dirname(__file__), 'data/emoji.json'), 'r') as full_data:
    emoji_data = [EmojiChar(data_blob) for data_blob in json.loads(full_data.read())]
    emoji_shortcodes = dict([(emoji.short_name.replace('-', '_'), emoji) for emoji in emoji_data])
    for emoji in emoji_data:
        for short_name in emoji.short_names:
            if short_name not in emoji_shortcodes:
                emoji_shortcodes[short_name] = emoji

from .main import replace_colons
