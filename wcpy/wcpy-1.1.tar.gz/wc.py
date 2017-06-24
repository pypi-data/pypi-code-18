#!/usr/bin/env python3

from wcpy.main import get_argument_parser
from wcpy.main import main

if __name__ == '__main__':
    parser = get_argument_parser()
    args = parser.parse_args()
    main(args)