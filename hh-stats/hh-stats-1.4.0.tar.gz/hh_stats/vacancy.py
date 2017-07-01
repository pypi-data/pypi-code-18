import json

import termcolor

from . import hh_api
from . import logger

class Salary:
    def __init__(self, minimal, maximal):
        self.minimal = minimal
        self.maximal = maximal

class Vacancy:
    def __init__(self, id_, skills, salary):
        self.id = id_
        self.skills = skills
        self.salary = salary

def process_vacancy(
    skills_delimiter,
    currency_rates,
    short_vacancy,
    delay,
    log_prefix,
):
    if short_vacancy['type']['id'] == 'closed':
        _warn_about_vacancy(short_vacancy, 'is closed')
        return None
    if short_vacancy['archived'] == True:
        _warn_about_vacancy(short_vacancy, 'is archived')
        return None

    full_vacancy = hh_api.request_hh_api(
        '/vacancies/' + short_vacancy['id'],
        {},
        delay,
        log_prefix,
    )
    if len(full_vacancy['key_skills']) == 0:
        _warn_about_vacancy(short_vacancy, "hasn't skills")
        return None

    return Vacancy(
        short_vacancy['id'],
        [
            skill
            for skill in (
                skill.strip()
                for skill_object in full_vacancy['key_skills']
                for skill in _separate_skill(
                    skill_object['name'],
                    skills_delimiter,
                    short_vacancy,
                )
            )
            if len(skill) > 0
        ],
        _convert_salary(currency_rates, full_vacancy['salary']),
    )

def _warn_about_vacancy(short_vacancy, message_end):
    logger.get_logger().warning(
        'vacancy %s %s',
        termcolor.colored(short_vacancy['id'], 'yellow'),
        message_end,
    )

def _separate_skill(skill, delimiter, short_vacancy):
    skills = delimiter.split(skill) if delimiter is not None else [skill]
    if len(skills) > 1:
        logger.get_logger().warning(
            'skill %s of the %s vacancy has been separated',
            termcolor.colored(json.dumps(skill, ensure_ascii=False), 'blue'),
            termcolor.colored(short_vacancy['id'], 'yellow'),
        )

    return skills

def _convert_salary(currency_rates, salary):
    if salary is None:
        return Salary(None, None)
    if salary['currency'] not in currency_rates:
        logger.get_logger().warning(
            'unknown currency %s',
            termcolor.colored(salary['currency'], 'green'),
        )
        return Salary(None, None)
    if salary['currency'] == 'RUR':
        return Salary(salary['from'], salary['to'])

    logger.get_logger().info(
        'converts %s to %s',
        termcolor.colored(salary['currency'], 'green'),
        termcolor.colored('RUB', 'green'),
    )
    if salary['from'] is not None:
        salary['from'] /= currency_rates[salary['currency']]
    if salary['to'] is not None:
        salary['to'] /= currency_rates[salary['currency']]

    return Salary(salary['from'], salary['to'])
