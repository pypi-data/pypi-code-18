import matplotlib.pyplot
import mpl_toolkits.axes_grid1
import termcolor

from .. import consts
from .. import logger

_BAR_WIDTH = 0.25
_PLOT_WIDTH_FACTOR = 0.64
_MINIMAL_PLOT_WIDTH = 6.4
_PLOT_ASPECT_RATIO = 1.33

def output_as_svg(stats_tuples, filename):
    _draw_plot(stats_tuples)
    _autoresize_plot(stats_tuples)

    if filename is not None:
        filename += '.svg'

        logger.get_logger().info(
            'writes the stats as %s to %s',
            termcolor.colored('SVG', 'green'),
            termcolor.colored(filename, 'green'),
        )
        matplotlib.pyplot.savefig(filename)
    else:
        logger.get_logger().info(
            'show the stats as %s',
            termcolor.colored('SVG', 'green'),
        )
        matplotlib.pyplot.show()

def _draw_plot(stats_tuples):
    skills, counters, minimal_salaries, maximal_salaries = zip(*stats_tuples)

    host_axis = mpl_toolkits.axes_grid1.host_subplot(111)
    host_axis.set_xticks(_make_indexes(stats_tuples, _BAR_WIDTH))
    host_axis.set_xticklabels(skills, rotation=90)
    host_axis.set_ylabel('Number')

    (counters_bar, *_) = host_axis.bar(
        _make_indexes(stats_tuples, 0),
        counters,
        _BAR_WIDTH,
        color='#9ac4f8',
    )

    right_axis = host_axis.twinx()
    right_axis.set_ylabel('Salary')

    (minimal_salaries_bar, *_) = right_axis.bar(
        _make_indexes(stats_tuples, _BAR_WIDTH),
        minimal_salaries,
        _BAR_WIDTH,
        color='#99edcc',
    )
    (maximal_salaries_bar, *_) = right_axis.bar(
        _make_indexes(stats_tuples, 2 * _BAR_WIDTH),
        maximal_salaries,
        _BAR_WIDTH,
        color='#cb958e',
    )
    host_axis.legend(
        (counters_bar, minimal_salaries_bar, maximal_salaries_bar),
        consts.STATS_TUPLE_ITEMS_NAMES[1:],
    )

    matplotlib.pyplot.xlim(
        -1.5 * _BAR_WIDTH,
        len(stats_tuples) - 1 + 3.5 * _BAR_WIDTH,
    )

def _make_indexes(stats_tuples, shift):
    return [index + shift for index in range(len(stats_tuples))]

def _autoresize_plot(stats_tuples):
    plot = matplotlib.pyplot.gcf()
    width = max(_PLOT_WIDTH_FACTOR * len(stats_tuples), _MINIMAL_PLOT_WIDTH)
    plot.set_size_inches(width, width / _PLOT_ASPECT_RATIO)
    plot.set_tight_layout(True)
