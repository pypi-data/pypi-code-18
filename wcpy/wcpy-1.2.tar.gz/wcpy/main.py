"""
This is the MAIN file from the wcpy module.
The parser is created in this file to, gathering all input from the
command line interface.
"""


from wcpy import WCCore, VERSION

import argparse

def get_argument_parser():
    """
    Create a parser with all the core options for the user to
    configure the input, processing and output of the word count.

    Returns:
        parser: Comtaining all the configuration to be displayed
    """
    parser = argparse.ArgumentParser(
        description='Count the number of words in the files on a folder',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""

EXAMPLE USAGE:
                wc.py ./
                wc.py ./ --limit 10
                wc.py doc1.txt doc2.txt --filter-words tool awesome an
                wc.py docs/ tests/ --truncate 100 --columns word count
                wc.py ./ --filter-words tool awesome an --truncate 50 --output output.txt
        """)
    parser.add_argument("paths", nargs="+", type=str,
        help="(REQUIRED) Path(s) to folders and/or files to count words from")
    parser.add_argument("-v", "--version", action="version",
        version="WordCount Python [ wc.py ] Version " + VERSION)
    parser.add_argument("--limit", type=int,
        help="(Optional) Limit the number of results that you would like to display.")
    parser.add_argument("--reverse", action="store_true",
        help="(Optional) List is sorted in ascending order by default, use this flag to reverse sorting to descending order.")
    parser.add_argument("--filter-words", nargs="+", type=str, default=[],
        help="(Optional) You can get results filtered to only the list of words provided.")
    parser.add_argument("--file-ext", type=str, default="txt",
        help="(Optional) This is the default file extention for the files being used")
    parser.add_argument("--truncate", type=int, default=50,
        help="(Optional) Output is often quite large, you can truncate the output by passing a number greater than 5")
    parser.add_argument("--columns", type=str, nargs="+", default=[],
        help="(Optional) This argument allows you to choose the columns to be displayed in the output. Options are: word, count, files and sentences.")
    parser.add_argument("--output-file", type=str,
        help="(Optional) Define an output file to save the output")

    return parser

def main(args):
    """
    Deploys a WCCore on the arguments that have been given through the
    command line interface.

    Raises:
        InvalidColumnException: When a column provided in the options is invalid
        PathNotValidException: When path provided does not exist or not valid
    """
    extractor = WCCore(
                    limit=args.limit,
                    direction=not(args.reverse),
                    filter_words=args.filter_words,
                    file_extension=args.file_ext,
                    output_file=args.output_file
                    )

    extractor.display_wc_table(args.paths, char_limit=args.truncate, columns=args.columns)



