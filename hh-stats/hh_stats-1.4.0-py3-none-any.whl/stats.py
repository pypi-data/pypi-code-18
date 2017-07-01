import json
import statistics

import jsonschema
import termcolor

from . import utils
from . import consts
from . import vacancy
from . import logger

class SalaryStats:
    def __init__(self):
        self.minimals = []
        self.maximals = []

class SkillStats:
    def __init__(self, counter, median_salary):
        self.counter = counter
        if median_salary is None:
            self.salary_stats = SalaryStats()
        else:
            self.median_salary = median_salary

_SKILLS_ALIASES_SCHEMA = {
    "type": "object",
    "patternProperties": {
        "^.+$": {
            "type": "array",
            "items": {
                "type": "string",
                "minLength": 1,
            },
            "uniqueItems": True,
            "minItems": 1,
        },
    },
    "additionalProperties": False,
    "minProperties": 1,
}

def collect_stats(vacancies, options):
    logger.get_logger().info(
        'collects a stats from %s vacancies',
        termcolor.colored(len(vacancies), 'yellow'),
    )

    unique_vacancies = utils.unique_everseen(
        vacancies,
        lambda vacancy: vacancy.id,
    )
    skills_aliases = _read_skills_aliases(options.skills_aliases)
    stats = _collect_stats_ex(
        unique_vacancies,
        skills_aliases,
        options.value_of_interest,
    )
    if len(stats) == 0:
        logger.get_logger().warning('stats is an empty')
        return None

    return stats

def convert_stats_to_tuples(stats, order):
    return sorted(
        [
            (
                skill,
                skill_stats.counter,
                skill_stats.median_salary.minimal,
                skill_stats.median_salary.maximal,
            )
            for skill, skill_stats in stats.items()
        ],
        key=lambda stats_tuple: stats_tuple[
            consts.STATS_TUPLE_ITEMS_MAP[order]
        ],
        reverse=True,
    )

def _read_skills_aliases(filename):
    if filename is None:
        return {}

    aliases = {}
    with open(filename) as aliases_file:
        aliases_data = json.load(aliases_file)
        jsonschema.validate(aliases_data, _SKILLS_ALIASES_SCHEMA)

        for skill, skill_aliases in aliases_data.items():
            for skill_alias in skill_aliases:
                aliases[skill_alias] = skill

    return aliases

def _collect_stats_ex(vacancies, skills_aliases, minimal_value):
    stats = {}
    for vacancy_ in vacancies:
        for skill in utils.unique_everseen(vacancy_.skills):
            resolved_skill = skills_aliases.get(skill, skill)
            if resolved_skill not in stats:
                stats[resolved_skill] = SkillStats(0, None)

            stats[resolved_skill].counter += 1
            stats[resolved_skill].salary_stats.minimals.append(
                vacancy_.salary.minimal,
            )
            stats[resolved_skill].salary_stats.maximals.append(
                vacancy_.salary.maximal,
            )

    return {
        skill: SkillStats(
            skill_stats.counter,
            vacancy.Salary(
                _get_median_salary(skill_stats.salary_stats.minimals),
                _get_median_salary(skill_stats.salary_stats.maximals),
            ),
        )
        for skill, skill_stats in stats.items()
        if skill_stats.counter >= minimal_value
    }

def _get_median_salary(salaries):
    salaries = [salary for salary in salaries if salary is not None]
    if len(salaries) == 0:
        return 0

    return round(statistics.median(salaries))
