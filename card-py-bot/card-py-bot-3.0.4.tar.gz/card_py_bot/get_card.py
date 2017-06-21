""" Handler module for parsing the wizzards website for metadata
on magic cards """

import os

from urllib.request import urlopen

import discord
import html5lib

from bs4 import BeautifulSoup


def make_mana_dict():
    mana_dict = dict()
    mana_colors_list = [
        'Green', 'Red', 'Blue', 'Black', 'White',
        'Phyrexian Blue', 'Phyrexian Red', 'Phyrexian Green',
        'Phyrexian Black', 'Phyrexian White',
        '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
        '11', '12', '13', '14', '15', '16', '1000000',
        'Black or Green', 'Red or White', 'Green or Blue',
        'Blue or Red', 'White or Black', 'White or Blue',
        'Blue or Black', 'Black or Red', 'Red or Green',
        'Green or White', 'Two or White', 'Two or Green',
        'Two or Black', 'Two or Red', 'Two or Blue',
        'Tap', 'Untap', 'Energy'
    ]

    config_file = open(os.path.dirname(
        os.path.abspath(__file__)) + '/' + 'mana_config.txt', "r")
    counter = 0

    for mana_emoji_id in config_file.readlines():
        mana_dict[mana_colors_list[counter]] = mana_emoji_id
        counter += 1

    config_file.close()
    return mana_dict


MANA_DICT = make_mana_dict()
WIZZARDS_BASE_URL = 'http://gatherer.wizards.com/'


def parse_cardtextbox(cardtextbox_div):
    """
    parse an arbitrary text box and also extract arbitrary elements
    like mana (objects and text)
    """
    # print("parse_cardtextbox:", cardtextbox_div)
    def extract_content(content):
        content_string = ""
        try:
            icon_content = content['alt']
            icon_string = MANA_DICT[icon_content].strip()
            return " " + icon_string + " "
        except (TypeError, KeyError):
            pass

        try:
            for content_prt in content.contents:
                content_string = content_string + extract_content(content_prt)
        except AttributeError:
            return content
        # print("parse_cardtextbox output:")
        return content_string

    content_string = extract_content(cardtextbox_div)

    # cleaning content_string for random newlines
    content_string = content_string.lstrip("\\n").strip()
    return content_string


def parse_base_value(value_div):
    """ parse out a simple element like an label value name (text) """
    # print("parse_base_value:",value_div)
    value_string = value_div.string.strip()
    # print("parse_base_value output:", value_string)
    import re
    value_string = re.sub('â€”', '--- ', value_string)
    return value_string


def parse_mana(mana_div):
    """ parse the mana cost of a card (objects) """
    mana_string = ""
    for mana_content in mana_div.children:
        try:
            mana_string = mana_string + \
                MANA_DICT[mana_content['alt']].strip() + " "
        except TypeError:
            pass
    # print("parse_mana output:", mana_string)
    return mana_string


def parse_image(image_div):
    """ parse the handler url for a card's image (url) """
    # print("parse_image:", image_div)
    image_handler = image_div.img['src'].lstrip('../../')
    # print("parse_image output:", image_handler)
    return image_handler


def parse_rarity(rarity_div):
    """ parse the rarity of a card (text) """
    # print("parse_rarity:", rarity_div)
    rarity = rarity_div.span.string
    # print("parse_rarity output:", rarity)
    return rarity


def parse_artist(artist_div):
    """ parse the artist name of a card (text) """
    # print("parse_artist:", artist_div)
    artist = artist_div.a.string
    # print("artist_div output:", artist)
    return artist


# TODO
def parse_expansion(expansion_div):
    """ parse the expansion name and set image handler (text and url) """
    pass


def scrape_wizzards(url='http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=74626'):
    """
    scrape a wotc magic card webpage and extract the cards details for
    embeding into a discord message
    """
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html5lib')

    label_dict = {
        'Community Rating': 'skip',
        'Card Name': parse_base_value,
        'Mana Cost': parse_mana,
        'Converted Mana Cost': parse_base_value,
        'Types': parse_base_value,
        'Card Text': parse_cardtextbox,
        'P/T': parse_base_value,
        'Expansion': 'skip',
        'Rarity': parse_rarity,
        'All Sets': 'skip',
        'Card Number': parse_base_value,
        'Artist': parse_artist,
        'Flavor Text': parse_cardtextbox
    }

    card_data = dict()
    label_list = soup.find_all('div', class_='label')
    for label_div in label_list:
        for string in label_div.stripped_strings:
            label_name = string.strip(':')
            try:
                if label_dict[label_name] != 'skip':
                    card_data[label_name] = \
                        label_dict[label_name](label_div.find_next_sibling('div'))
            except KeyError:
                print("unrecognised label:", label_name)
                pass

    card_image_div = soup.find('div', class_='cardImage')
    card_data['image_url'] = WIZZARDS_BASE_URL + parse_image(card_image_div)
    return card_data


def card_data2string(card_data):
    """
    take scraped card data and convert it into a raw string for discord
    """

    element_list = ['Card Name', 'Mana Cost', 'Types', 'Rarity', 'Card Text',
                    'Flavor Text', 'P/T', 'Artist', 'image_url']
    out_string = ''
    for element in element_list:
        if element in card_data:
            if element == 'image_url':
                out_string = out_string + card_data[element]
            elif element == 'Flavor Text':
                out_string = out_string + '**' + element + ":**" +\
                             '*' + card_data[element] + '*\n'
            else:
                out_string = out_string + '**' + element + ":** " +\
                             card_data[element] + '\n'

    return out_string


def card_data2embed(card_data, in_url, avatar_url):
    """
    take scraped card data and format it into a discord embed
    """

    element_list = ['Mana Cost', 'Types', 'Rarity', 'Card Text',
                    'Flavor Text', 'P/T', 'Artist', 'image_url']

    try:
        card_name = card_data['Card Name']
        embed_title = '**Card Name**\n[{}]({})'.format(card_name, in_url)
    except:
        embed_title = 'Error: giving raw url:' + in_url

    em = discord.Embed(description=embed_title, colour=0xDEADBF)
    em.set_footer(text='card-py-bot by Nathan Klapstein', icon_url=avatar_url)
    # em.set_thumbnail(url=avatar_url)
    for element in element_list:
        if element in card_data:
            if element == 'image_url':
                em.set_image(url=card_data[element])
            elif element == 'Flavor Text':
                em.add_field(name=element, value='*' + card_data[element] + '*')
            else:
                em.add_field(name=element, value=card_data[element], inline=False)

    return em
