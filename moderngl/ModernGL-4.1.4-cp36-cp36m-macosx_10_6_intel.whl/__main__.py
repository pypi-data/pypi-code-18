'''
    ModernGL main
'''

import argparse

import ModernGL


def main():
    '''
        main
    '''

    parser = argparse.ArgumentParser(prog='ModernGL')
    parser.add_argument('-v', '--version', action='version', version='ModernGL %s' % ModernGL.__version__)
    parser.parse_args()

    ctx = ModernGL.create_standalone_context()

    print('ModernGL:', ModernGL.__version__)
    print('Vendor:', ctx.vendor)
    print('Renderer:', ctx.renderer)
    print('Version:', ctx.version)


if __name__ == '__main__':
    main()
