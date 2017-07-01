import sys

from . import cli
from . import hh_api_ex
from . import input_
from . import stats
from . import logger
from .output import raw
from .output import csv
from .output import svg

def main():
    logger.init_logger()

    try:
        options = cli.parse_options()
        if options.inputs is None:
            vacancies = hh_api_ex.request_vacancies(options)
        else:
            vacancies = input_.read_vacancies(options.inputs)
        if vacancies is None:
            return
        if 'raw' in options.format:
            raw.output_as_raw(vacancies, options.output)
            if len(options.format) == 1:
                return

        stats_ = stats.collect_stats(vacancies, options)
        if stats_ is None:
            return

        stats_tuples = stats.convert_stats_to_tuples(stats_, options.order)
        if 'csv' in options.format:
            csv.output_as_csv(stats_tuples, options.output)
        if 'svg' in options.format:
            svg.output_as_svg(stats_tuples, options.output)
    except Exception as exception:
        logger.get_logger().error(exception)
        sys.exit(1)
    except KeyboardInterrupt:
        # output a line break after the ^C symbol in a terminal
        print('')

        sys.exit(1)
