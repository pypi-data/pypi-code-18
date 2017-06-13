import argparse

def parser():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--language1', dest='lang', metavar='བོད་སྐད་ལ་', type=str, help='Lanugage for output')
    parser.add_argument('--language2', dest='lang', metavar='LANGUAGE', type=str, help='Lanugage for output')
    return parser.parse_args()
