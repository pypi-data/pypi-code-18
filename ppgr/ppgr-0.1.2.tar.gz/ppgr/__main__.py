import argparse
import sys

from .ppgr import PPGR, no_cursor


def main():
    parser = argparse.ArgumentParser(
        description="terminal graphing tool that supports piped data with realtime updates")

    parser.add_argument(
        "-f", "--format",
        nargs="+",
        default=["a"],
        choices=("a", "t", "d", "s"))
    parser.add_argument(
        "-x", "--fail-bad-line",
        action="store_true",
        help="fail if input line can't be parsed")
    parser.add_argument(
        "-w", "--wait",
        type=int,
        metavar="N",
        help="wait at least N milliseconds between frames")
    parser.add_argument(
        "-t", "--time-scale",
        type=float)
    parser.add_argument(
        "-l", "--limit",
        type=int)
    parser.add_argument(
        "-s", "--no-animate",
        action="store_true")
    parser.add_argument(
        "-i", "--input",
        type=argparse.FileType("r"),
        default="-")

    parser.add_argument(
        "--max-x",
        type=float)
    parser.add_argument(
        "--min-x",
        type=float)
    parser.add_argument(
        "--max-y",
        type=float)
    parser.add_argument(
        "--min-y",
        type=float)

    argv = parser.parse_args()
    ppgr = PPGR(
        argv.format,
        argv.fail_bad_line,
        argv.wait,
        argv.time_scale,
        argv.limit)

    with no_cursor():
        for line in argv.input:
            ppgr.line(line)
            if not argv.no_animate:
                ppgr.show(argv.max_x, argv.min_x, argv.max_y, argv.min_y)
        if argv.no_animate:
            ppgr.show(argv.max_x, argv.min_x, argv.max_y, argv.min_y, True)

try:
    main()
except KeyboardInterrupt:
    sys.exit(0)
