import functools
import re

import termcolor

from . import vacancy
from . import hh_api
from . import consts
from . import logger

_LOG_TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

def request_vacancies(options):
    skills_delimiter = _compile_skills_delimiter(options.skills_delimiters)
    currency_rates = _request_currency_rates(1 / options.request_frequency)
    vacancies, total_number = _request_vacancies_for_period(
        {
            'area': options.areas,
            'specialization': options.specializations,
            'text': options.query,
            'search_field': options.query_properties,
            'only_with_salary': options.salary_required,
        },
        options.analysis_begin,
        options.analysis_end,
        options.analysis_increment,
        1 / options.request_frequency,
        options.error_on_limit,
        options.page_size,
        functools.partial(
            vacancy.process_vacancy,
            skills_delimiter,
            currency_rates,
        ),
    )
    if len(vacancies) == 0:
        logger.get_logger().warning("suitable vacancies hasn't been found")
        return None

    logger.get_logger().info(
        '%s/%s suitable vacancies has been found',
        termcolor.colored(str(len(vacancies)), 'yellow'),
        termcolor.colored(str(total_number), 'yellow'),
    )
    return vacancies

def _compile_skills_delimiter(skills_delimiters):
    skills_delimiter = None
    if len(skills_delimiters) > 0:
        skills_delimiter = re.compile(
            '[{:s}]'.format(re.escape(''.join(skills_delimiters))),
        )

    return skills_delimiter

def _request_currency_rates(delay):
    dictionaries = hh_api.request_hh_api('/dictionaries', {}, delay, '')
    return {
        currency['code']: currency['rate']
        for currency in dictionaries['currency']
    }

def _request_vacancies_for_period(
    parameters,
    period_begin,
    period_end,
    increment,
    delay,
    error_on_limit,
    page_size,
    item_handler,
):
    request_all_pages_for_period = lambda start, end: \
        hh_api.handle_hh_api_pagination(
            '/vacancies',
            {
                **parameters,
                'date_from': start.strftime(consts.TIMESTAMP_FORMAT),
                'date_to': end.strftime(consts.TIMESTAMP_FORMAT),
            },
            delay,
            'period {:s}-{:s}; '.format(
                termcolor.colored(
                    str(start.strftime(_LOG_TIMESTAMP_FORMAT)),
                    'magenta',
                ),
                termcolor.colored(
                    str(end.strftime(_LOG_TIMESTAMP_FORMAT)),
                    'magenta',
                ),
            ),
            error_on_limit,
            page_size,
            item_handler,
        )
    if increment is None:
        return request_all_pages_for_period(period_begin, period_end)

    total_vacancies = []
    total_number = 0
    start_timestamp = period_begin
    end_timestamp = start_timestamp + increment
    while start_timestamp < period_end:
        clamped_end_timestamp = min(end_timestamp, period_end)
        vacancies, number = request_all_pages_for_period(
            start_timestamp,
            clamped_end_timestamp,
        )
        total_vacancies += vacancies
        total_number += number

        start_timestamp += increment
        end_timestamp += increment

    return total_vacancies, total_number
