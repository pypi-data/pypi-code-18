import json
import sys

import termcolor

from .. import vacancy
from .. import logger

class VacancyEncoder(json.JSONEncoder):
    def default(self, object_):
        if any(
            isinstance(object_, class_)
            for class_ in [vacancy.Vacancy, vacancy.Salary]
        ):
            return object_.__dict__

        return json.JSONEncoder.default(self, object_)

def output_as_raw(vacancies, filename):
    if filename is not None:
        with open(filename + '.raw.json', 'w') as raw_file:
            _write_as_raw(vacancies, raw_file)
    else:
        _write_as_raw(vacancies, sys.stdout)

def _write_as_raw(vacancies, stream):
    logger.get_logger().info(
        'writes raw vacancies to %s',
        termcolor.colored(str(stream), 'blue'),
    )

    json.dump(
        vacancies,
        stream,
        ensure_ascii=False,
        indent=2,
        separators=(',', ': '),
        cls=VacancyEncoder,
    )
