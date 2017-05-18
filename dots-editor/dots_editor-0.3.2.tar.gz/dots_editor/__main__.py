import sys, argparse
from . import core

def main(args=None):
    if args is None:
        args = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", default="out.txt", help="the name of the file to save")
    parser.add_argument("--encoding", default="ascii", help="the encoding to use - default ascii (.brl)")
    parser.add_argument("--unicode", action="store_const", const="utf8", dest="encoding", help="use unicode encoding")
    args = parser.parse_args(args)
    game = core.Game(args.filename, args.encoding)
    game.loop()

if __name__ == "__main__":
    main()
