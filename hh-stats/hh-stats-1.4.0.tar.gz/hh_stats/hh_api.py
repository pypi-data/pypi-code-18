import time
import urllib.parse

import requests
import termcolor

from . import consts
from . import logger

_HH_API_HEADERS = {
    'User-Agent': '{:s} v{:s} (thewizardplusplus@yandex.ru)'.format(
        consts.APP_NAME,
        consts.APP_VERSION,
    ),
}
_HH_API_SEARCH_LIMIT = 2000

def request_hh_api(endpoint, parameters, delay, log_prefix):
    logger.get_logger().info(
        '%srequests %s with parameters %s',
        log_prefix,
        termcolor.colored(endpoint, 'green'),
        termcolor.colored(str(parameters), 'blue'),
    )
    time.sleep(delay)

    url = urllib.parse.urljoin('https://api.hh.ru/', endpoint)
    response = requests.get(url, params=parameters, headers=_HH_API_HEADERS)
    data = response.json()
    if 'errors' in data:
        raise Exception(_format_hh_api_errors(data['errors']))

    return data

def handle_hh_api_pagination(
    endpoint,
    parameters,
    delay,
    log_prefix,
    error_on_limit,
    page_size,
    item_handler,
):
    items = []
    current_page = 0
    current_item = 0
    pages_number = None
    while True:
        data = request_hh_api(
            endpoint,
            {**parameters, 'per_page': page_size, 'page': current_page},
            delay,
            '{:s}page {:s}/{:s}: '.format(
                log_prefix,
                termcolor.colored(str(current_page + 1), 'yellow'),
                termcolor.colored(
                    str(pages_number) if pages_number is not None else '?',
                    'yellow',
                ),
            ),
        )
        if 'items' not in data:
            logger.get_logger().warning("endpoint isn't paginated")
            data = {'items': [data], 'page': 0, 'pages': 1, 'found': 1}
        if data['found'] > _HH_API_SEARCH_LIMIT:
            message = 'the search limit has been exceeded'
            if not error_on_limit:
                logger.get_logger().warning(message)
            else:
                raise Exception(message)

        for item in data['items']:
            current_item += 1
            handled_item = item_handler(
                item,
                delay,
                'item {:s}/{:s}: '.format(
                    termcolor.colored(str(current_item), 'yellow'),
                    termcolor.colored(
                        str(min(data['found'], _HH_API_SEARCH_LIMIT)),
                        'yellow',
                    ),
                )
            )
            if handled_item is not None:
                items.append(handled_item)

        current_page += 1
        pages_number = data['pages']
        if current_page == pages_number:
            break

    return items, current_item

def _format_hh_api_errors(errors):
    formatted_errors = [_format_hh_api_error(error) for error in errors]
    return 'HH API errors: ' + ', '.join(formatted_errors)

def _format_hh_api_error(error):
    formatted_error = termcolor.colored(error['type'], 'red')
    if 'value' in error:
        formatted_error += '/' + termcolor.colored(error['value'], 'red')

    return formatted_error
