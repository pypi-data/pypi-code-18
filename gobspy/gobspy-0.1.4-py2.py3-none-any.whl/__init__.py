import lang
from lang.utils import read_file
import lang.i18n as i18n
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Execute Gobspy.')
    parser.add_argument('file')
    parser.add_argument('-l', '--language', default='es',
        help='language used for code translation')

    args = parser.parse_args()
    return args



def main():
    args = parse_args()
    i18n.set_language(args.language
    )
    lang.run(read_file(args.file), args.file)
    print(lang.state.board)

if __name__ == '__main__':
    main()
