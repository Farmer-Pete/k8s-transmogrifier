'''
Transmogrifier - Translates config files into code and reports
'''

import lib.cmdline
import plugins.transmogrifiers


def main():
    ''' The main method '''

    args = lib.cmdline.command_line_parser.parse_args()

    plugins.transmogrifiers.execute(args)


if __name__ == '__main__':
    main()
    print("Done")

