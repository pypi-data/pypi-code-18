""" Plugin entry point for helga """
from amazon.api import AmazonAPI
from helga import settings
from helga.plugins import match


PRODUCT_REGEX = r'amazon\.com/(?:[\w|-]+/)?dp/(\w+)'


@match(PRODUCT_REGEX)
def amazon_meta(client, channel, nick, message, match):
    return generate_amazon_response(match)


def generate_amazon_response(product_id):
    if not settings.AMAZON_ACCESS_KEY or not settings.AMAZON_SECRET_KEY or not settings.AMAZON_ASSOC_TAG:
        return 'Amazon API keys not set, please add to your settings'
    amazon = AmazonAPI(settings.AMAZON_ACCESS_KEY, settings.AMAZON_SECRET_KEY, settings.AMAZON_ASSOC_TAG)
    product = amazon.lookup(ItemId=match)
    return 'Title: {} Price: {}'.format(product.title, product.price)
