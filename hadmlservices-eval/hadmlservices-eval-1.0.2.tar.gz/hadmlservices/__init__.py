import os
import sys
from argparse import ArgumentParser
from hadmlservices import service


def make_parser():
    parser = ArgumentParser()
    parser.add_argument(
        'root_dir',
        help="Root of the directory tree for user_data execution."
    )
    parser.add_argument(
        'predictioni_dir',
        help="Directory containing prediction."
    )
    parser.add_argument(
        'truth_dir',
        help="Directory containing truth."
    )
    parser.add_argument(
        'output_dir',
        help="Directory to save the execution output."
    )
    parser.add_argument(
        '--params',
        default=None,
        help="Parameters (if any) combined into a single string"
    )
    return parser

def main():
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
    arg_parser = make_parser()
    args = arg_parser.parse_args()
    service.user_data(args.root_dir,
                      args.prediction_dir,
                      args.truth_dir,
                      args.output_dir,
                      args.model_params)
