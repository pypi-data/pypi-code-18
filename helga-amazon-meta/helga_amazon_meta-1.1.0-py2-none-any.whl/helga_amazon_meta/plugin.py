""" Plugin entry point for helga """
import re

import requests
from amazon.api import AmazonAPI
from bs4 import BeautifulSoup

from helga import settings
from helga.plugins import match


PRODUCT_REGEX = r'amazon\.com/(?:[\w|-]+/)?dp/(\w+)'
PRUDUCT_URL = 'https://www.amazon.com/dp/'
RESPONSE_TEMPLATE = 'Title: {} Price: {}'
SHORT_REGEX = r'(a.co/\w+)'


@match(PRODUCT_REGEX)
def amazon_meta(client, channel, nick, message, match):
    return parse_response(match) or generate_amazon_response(match)


@match(SHORT_REGEX)
def amazon_meta_short(client, channel, nick, message, match):
    return handle_short_link(match)


def handle_short_link(url):
    response = requests.get('http://' + url)
    url = response.url
    match = re.search(PRODUCT_REGEX, url)
    product_id = match.group(1)
    product_info_response = parse_response(response.text)
    return parse_response(match, response.text) or generate_amazon_response(product_id)


def parse_response(product_id, body=None):
    """ Parse a response for title and price """
    if body is None:
        body = requests.get(PRUDUCT_URL + product_id).text
    soup = BeautifulSoup(body, "html.parser")
    title = soup.title.text.replace('Amazon.com: ', '')
    title_select = soup.select('#title')
    if title_select:
        title = title_select[0].text.strip()
    price = soup.select('#priceblock_ourprice')
    if price:
        price = price[0].text.strip()
    if title and price:
        return RESPONSE_TEMPLATE.format(title, price)
    return None


def generate_amazon_response(product_id):
    if not settings.AMAZON_ACCESS_KEY or not settings.AMAZON_SECRET_KEY or not settings.AMAZON_ASSOC_TAG:
        return 'Amazon API keys not set, please add to your settings'
    amazon = AmazonAPI(settings.AMAZON_ACCESS_KEY, settings.AMAZON_SECRET_KEY, settings.AMAZON_ASSOC_TAG)
    product = amazon.lookup(ItemId=match)
    return RESPONSE_TEMPLATE.format(product.title, product.price)
